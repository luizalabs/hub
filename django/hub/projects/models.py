# coding: utf-8
import json
import logging
import urllib

import markdown
import requests

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from taggit.managers import TaggableManager

from accounts.models import Account
from teams.models import Team
from utils import notify
from utils.email import send_email_template
from utils.softdelete import SoftDeleteManager, SoftDeleteMixin


logger = logging.getLogger('projects.models')


class Project(models.Model, SoftDeleteMixin):
    parent = models.ForeignKey('self', related_name='applications',
                           null=True, blank=True, verbose_name='Produto')
    name = models.CharField(u'nome', max_length=32)
    headline = models.CharField(u'headline', max_length=64, blank=True,
                                help_text=u'Ex.: "Plataforma de recomendações"')
    description = models.TextField(u'descrição', help_text=u'Utilize formatação Markdown')

    team = models.ForeignKey(Team, null=True, blank=True, verbose_name=u'time mantenedor')
    added_by = models.ForeignKey(Account, related_name='added_projects')
    members = models.ManyToManyField(Account, null=True, blank=True,
                                     verbose_name=u'pessoas que passaram pelo projeto')

    repo_id = models.CharField(u'repositório Github (org/repo_name)', blank=True, max_length=32,
                               help_text=u'Inclua a organização, exemplo: "luizalabs/p36"')
    travis_enabled = models.BooleanField(u'Incluir badge do Travis CI', default=False)

    image = models.ImageField(
        u'logotipo', upload_to='projects/', blank=True,
        help_text=u'Todo projeto precisa de um logotipo! Envie imagens quadradas (~500x500px)',
    )
    created_at = models.DateTimeField(default=now)
    tags = TaggableManager(verbose_name=u'tags')

    def __unicode__(self):
        return self.name

    @property
    def github(self):
        return 'https://github.com/{}'.format(self.repo_id)

    def render_description(self):
        return markdown.markdown(self.description)

    @property
    def changelogs(self):
        if not self.parent:
            return Changelog.objects.filter(
                models.Q(project=self) |
                models.Q(project__in=self.applications.all())
            )
        return self.changelog_set.all()


class Changelog(models.Model, SoftDeleteMixin):
    project = models.ForeignKey(Project)
    email_recipients = models.TextField(u'Destinatários', blank=True,
                                        help_text='Separe os e-mails por vírgula')
    email_subject = models.CharField(u'assunto do e-mail', max_length=64, blank=True,
                                     help_text=u'Ex.: "Changelog - Stewie - Sprint 3"')

    description = models.TextField(u'descrição', help_text=u'Escreva em português. Utilize formatação Markdown.')

    added_by = models.ForeignKey(Account, related_name='added_changelogs')
    created_at = models.DateTimeField(default=now)
    email_sent = models.BooleanField(u'e-mail enviado', default=False)
    last_slack_payload = models.CharField(u'última mensagem para o slack',
                                          max_length=512, blank=True,
                                          null=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.email_subject

    def render_description(self):
        return markdown.markdown(self.description)

    def send_mail(self):
        if self.email_sent is False:
            send_email_template(
                subject=self.email_subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[e.strip() for e in
                                self.email_recipients.split(',')],
                template='projects/changelog_email.html',
                context={
                    'changelog': self,
                }
            )
            self.email_sent = True
            self.save()

    def send_slack(self, **kwargs):
        self.last_slack_payload = notify.slack(**kwargs)
        self.save()

    @property
    def reactions(self):
        slack_info = json.loads(self.last_slack_payload)
        slack_info['token'] = settings.CHANGELOG_API_TOKEN

        get_reactions_url = u'https://slack.com/api/reactions.get?{}'
        reactions = requests.get(get_reactions_url.format(
            urllib.urlencode(slack_info)
        ))
        reactions = json.loads(reactions.text)
        reactions = reactions.get('message', {}).get('reactions', [])
        data = {}
        for reaction in reactions:
            if reaction['name'] == '+1':
                data['thumbs_up_count'] = reaction['count']
            elif reaction['name'] == '-1':
                data['thumbs_down_count'] = reaction['count']
        return data
