# coding: utf-8
import logging
from django.db import models
from utils.softdelete import SoftDeleteMixin


logger = logging.getLogger('teams.models')


class Area(models.Model, SoftDeleteMixin):
    leader = models.ForeignKey('accounts.Account', related_name='area_set',
                               verbose_name=u'líder da área')
    name = models.CharField(u'nome', max_length=64)

    def __unicode__(self):
        return self.name


class Team(models.Model, SoftDeleteMixin):
    area = models.ForeignKey(Area, verbose_name=u'área')
    leader = models.ForeignKey('accounts.Account', related_name='team_set',
                               verbose_name=u'líder do time')
    name = models.CharField(u'nome', max_length=64)

    image = models.ImageField(
        u'foto', upload_to='teams/', blank=True,
        help_text=u'Tire uma foto do seu time! Envie imagens quadradas (~500x500px)',
    )

    class Meta:
        ordering = ('area', 'name')

    def __unicode__(self):
        return u'{} - {}'.format(self.area, self.name)
