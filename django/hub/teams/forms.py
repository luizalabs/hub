# coding: utf-8
from django import forms
from models import Team


class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Team


class TeamUpdateForm(forms.ModelForm):

    class Meta:
        model = Team
