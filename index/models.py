from django.db import models
import math


class SmartWord(models.Model):
    word_one = models.CharField(verbose_name="Слово первое", max_length=100)
    word_two = models.CharField(verbose_name="Слово второе", max_length=100, default='', null=False)
    weight2 = models.IntegerField(verbose_name="Вес", default=0)
    positive_count = models.IntegerField(
        verbose_name="Количество документов с положительной оценкой", 
        default=1)
    negative_count = models.IntegerField(
        verbose_name="Количество документов с отрицательной оценкой", 
        default=1)

    def __str__(self):
        if self.word_two:
            return self.word_one + ' ' + self.word_two
        return self.word_one

    def weight(self, count_in_document=1):
        return count_in_document * math.log(self.positive_count / self.negative_count, 2)

    def weight_solo(self):
        return math.log(self.positive_count / self.negative_count, 2)
