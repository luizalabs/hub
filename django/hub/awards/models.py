# coding: utf-8
from django.db import models
from django.utils import timezone

from accounts.models import Account
from utils.softdelete import SoftDeleteMixin


class Award(models.Model, SoftDeleteMixin):

    name = models.CharField(u'nome do prêmio', max_length=255)
    image = models.ImageField(
        u'foto', upload_to='awards/',
        help_text=u'Foto para simbolizar o prêmio que a pessoa ganhou 128x128px.',
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name


class AccountAward(models.Model, SoftDeleteMixin):
    account = models.ForeignKey(Account, related_name='awards')
    award = models.ForeignKey(Award)

    title = models.CharField(u'Nome do prêmio para o usuário', max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    awarded_by = models.ForeignKey(Account, related_name=u'awards_given')

    def __unicode__(self):
        return self.title
