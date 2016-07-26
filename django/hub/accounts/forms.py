# coding: utf-8

from django import forms

from models import Account
from utils.cleantags import CleanTagsMixin


class ProfileUpdateForm(CleanTagsMixin, forms.ModelForm):
    reports_to = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        empty_label='-' * 8,
        required=False,
    )

    birth_date = forms.DateField(
        label=u'Data de Aniversário',
        input_formats=['%d/%M/%Y'],
        help_text=u'Ex: 20/10/1990'
    )

    class Meta:
        fields = ('reports_to', 'team', 'name', 'birth_date', 'branch', 'phone',
                  'github_username', 'twitter_username', 'image', 'tags',
                  'starting_date', 'leaving_date')
        model = Account

    def __init__(self, request, *args, **kwargs):
        ret = super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if not request.user.is_superuser:
            del self.fields['starting_date']
            del self.fields['leaving_date']
        return ret

    def clean_reports_to(self):
        if self.cleaned_data['reports_to'] == self.instance:
            raise forms.ValidationError(u'Mas só pode estar de brincanagem! Você não pode ser seu próprio chefe!')
        return self.cleaned_data['reports_to']
