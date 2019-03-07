from django.shortcuts import render, HttpResponse
from index.forms import ParserForm, QuestionForm
from index.models import SmartWord
import re


def parser(request):
    form = ParserForm()
    ctx = {'form': form}
    if request.method == 'POST':

        form = ParserForm(request.POST)

        if form.is_valid():
            # Берём текст и его оценку 
            text = form.cleaned_data['text']
            action = form.cleaned_data['action']

            # Разбиваем текст на слова и переводим в ловеркейс
            text = re.findall(r'([а-яА-Я]+)', text)
            text = list(map(lambda x: x.lower(), text))

            # Массивы для вывода
            unigram_words = []
            bigram_words = []

            # Присваеваем веса словам в зависимости от оценки
            for index, text_word in enumerate(text):
                next_word = text[index+1] if index+1 < len(text) else ''

                # расчёт весов для униграмы
                unigram, _ = SmartWord.objects.get_or_create(word_one=text_word, word_two='')
                if action == 'good':
                    unigram.positive_count += 1
                elif action == 'bad':
                    unigram.negative_count += 1
                unigram.save()
                unigram_words.append(unigram)

                # Расчёт весов для биграмы
                if next_word:
                    bigram, _ = SmartWord.objects.get_or_create(word_one=text_word, word_two=next_word)
                    if action == 'good':
                        bigram.positive_count += 1
                    elif action == 'bad':
                        bigram.negative_count += 1
                    bigram.save()
                    bigram_words.append(bigram)

            
            ctx['unigram_words'] = unigram_words
            ctx['bigram_words'] = bigram_words
            

    return render(request, 'index/parser.html', ctx)


def answer(request):
    form = QuestionForm()
    ctx = {'form': form}
    if request.method == 'POST':
        form = ParserForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            previous_text = text
            value_unigram = 0
            value_bigram = 0
            value_combined = 0
            value_prior_bigram = 0

            # Разбиваем текст на слова и переводим в ловеркейс
            text = re.findall(r'([а-яА-Я]+)', text)
            text = list(map(lambda x: x.lower(), text))

            # Расчёт весов униграм
            unigram_words = SmartWord.objects.filter(word_one__in=text, word_two='')
            for unigram_word in unigram_words:
                value_unigram += unigram_word.weight(text.count(unigram_word.word_one))

            # Расчёт весов биграм
            for index in range(len(text) - 1):
                bigram_word = SmartWord.objects.filter(word_one=text[index], word_two=text[index + 1]).first()
                if bigram_word:
                    # TODO: подредактировать вычисление количетсва вхождений словосочетаний
                    value_bigram += bigram_word.weight(text.count(text[index]) + text.count(text[index + 1]))

            # Расчёт совместных вычислений
            value_combined = value_unigram + value_bigram

            # Расчёт где биграмы в приотитете
            index = 0
            while (True):
                if index >= len(text) - 1:
                    break
                bigram_word = SmartWord.objects.filter(word_one=text[index], word_two=text[index + 1]).first()
                unigram_word = SmartWord.objects.filter(word_one=text[index], word_two='').first()

                if bigram_word:
                    value_prior_bigram += bigram_word.weight(text.count(text[index]) + text.count(text[index + 1]))
                elif unigram_word:
                    value_prior_bigram += unigram_word.weight(text.count(text[index]))

                index += 1

            if value_unigram < 0:
                ctx['answer_unigram'] = "Стресс"
            else:
                ctx['answer_unigram'] = "Всё в порядке"
            ctx['answer_unigram_value'] = value_unigram

            if value_bigram < 0:
                ctx['answer_bigram'] = "Стресс"
            else:
                ctx['answer_bigram'] = "Всё в порядке"
            ctx['answer_bigram_value'] = value_bigram

            if value_combined < 0:
                ctx['answer_combined'] = "Стресс"
            else:
                ctx['answer_combined'] = "Всё в порядке"
            ctx['answer_combined_value'] = value_combined

            if value_prior_bigram < 0:
                ctx['answer_prior_bigram'] = "Стресс"
            else:
                ctx['answer_prior_bigram'] = "Всё в порядке"
            ctx['answer_prior_bigram_value'] = value_prior_bigram
            
            ctx['previous_text'] = previous_text

    return render(request, 'index/answer.html', ctx)
