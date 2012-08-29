# -*- coding: utf-8 -*-
from django.forms import ModelForm
from service.models import Question

class QuestionForm(ModelForm):
   
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['phone'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['subject'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['content'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['name'].widget.attrs['class'] = 'input-xxxlarge'

    class Meta:
        model = Question
        exclude = ('user', 'status')
