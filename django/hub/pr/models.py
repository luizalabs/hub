# coding: utf-8
import logging
from django.db import models
from django.utils.timezone import now
from accounts.models import Account
from teams.models import Team
from utils.softdelete import SoftDeleteMixin


logger = logging.getLogger('pr.models')


class PressRelease(models.Model, SoftDeleteMixin):
    added_by = models.ForeignKey(Account, related_name='added_releases')
    title = models.CharField(u'título', max_length=64)
    author_name = models.CharField(u'nome do autor', max_length=32)
    author_email = models.EmailField(u'e-mail do autor')
    text = models.TextField(u'texto')

    teams = models.ManyToManyField(Team, verbose_name=u'times envolvidos')

    created_at = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.title


class Question(models.Model, SoftDeleteMixin):
    author = models.ForeignKey(Account, related_name='questions')
    press_release = models.ForeignKey(PressRelease)
    question = models.TextField(u'pergunta')
    answer = models.TextField(
        u'resposta', blank=True,
        help_text=u'Não sabe a resposta ainda? Deixe em branco e alguém responderá')
    created_at = models.DateTimeField(default=now)
