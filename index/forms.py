from django import forms


class ParserForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        if 'good' in self.data:
            self.cleaned_data['action'] = 'good'
        elif 'bad' in self.data:
            self.cleaned_data['action'] = 'bad'
        return super(ParserForm, self).clean()


class QuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)
    
