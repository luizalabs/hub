# coding: utf-8
from django import forms

from models import AccountAward


class AccountAwardForm(forms.ModelForm):

    class Meta:
        model = AccountAward
        exclude = ('account', 'awarded_by', 'created_at')
