# coding: utf-8

from django import forms

from .models import PressRelease, Question


class PressReleaseForm(forms.ModelForm):

    class Meta:
        model = PressRelease
        exclude = ('added_by', 'created_at')


class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question', 'answer')


class QuestionUpdateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question', 'answer')
