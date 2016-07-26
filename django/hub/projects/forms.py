# coding: utf-8

from django import forms

from models import Changelog, Project
from utils.cleantags import CleanTagsMixin
from utils.validators import validate_email_list


class ProjectForm(CleanTagsMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        qs = Project.objects.filter(parent=None)
        self.fields['parent'].queryset = qs

        if self.instance:
            self.fields['parent'].queryset = qs.exclude(pk=self.instance.pk)

        if self.instance.parent or self.initial.get('parent'):
            self.fields['parent'].widget = forms.HiddenInput()

    class Meta:
        model = Project
        exclude = ('added_by', 'created_at')


class ChangelogForm(forms.ModelForm):
    email_recipients = forms.CharField(
        label=u'Destinatários',
        required=False,
        widget=forms.Textarea,
        validators=[validate_email_list]
    )
    send_mail = forms.BooleanField(label=u'Enviar e-mail', required=False)

    class Meta:
        model = Changelog
        fields = ('send_mail', 'email_recipients', 'email_subject',
                  'description')


class SendMailChangelogForm(forms.ModelForm):
    email_recipients = forms.CharField(
        label=u'Destinatários',
        required=False,
        widget=forms.Textarea,
        validators=[validate_email_list]
    )

    class Meta:
        model = Changelog
        fields = ('email_recipients', 'email_subject')


class SendSlackForm(forms.Form):
    channel = forms.CharField(
        label=u'Canal',
        help_text=u'Iniciar nome de canal com #, usuários com @, '
                  u'se enviar para múltiplos canais ou usuários, separá-los '
                  u'por vírgula'
    )

    class Meta:
        fields = ('channel',)
