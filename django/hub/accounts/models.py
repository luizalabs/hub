# coding: utf-8
import logging
from dateutil import relativedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from teams.models import Team
from utils.softdelete import SoftDeleteMixin


logger = logging.getLogger('accounts.models')


class CompanyBranch(models.Model, SoftDeleteMixin):
    name = models.CharField(u'nome', max_length=32)

    def __unicode__(self):
        return self.name


class ActiveUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        return super(ActiveUserManager, self) \
            .get_queryset(*args, **kwargs).filter(leaving_date__isnull=True)


class Account(MPTTModel, AbstractBaseUser, PermissionsMixin):

    """
    An account represents an employee
    """
    USERNAME_FIELD = 'email'

    reports_to = TreeForeignKey(
        'self', null=True, blank=True,
        related_name='account_set', verbose_name=u'líder direto',
    )
    branch = models.ForeignKey(
        CompanyBranch, max_length=16, null=True,
        verbose_name=u'filial'
    )
    team = models.ForeignKey(Team, null=True, blank=True, verbose_name=u'time')
    name = models.CharField(u'nome', max_length=128)

    phone = models.CharField(u'telefone', max_length=32, blank=True)
    github_username = models.CharField(u'Github (pessoal)', max_length=50, blank=True)
    twitter_username = models.CharField(u'Twitter', max_length=50, blank=True)

    image = models.ImageField(
        u'foto', upload_to='accounts/', blank=True,
        help_text=u'Escolha uma foto real e atual, para que seja identificado - ex.: não coloque a foto do Darth Vader. Envie imagens quadradas (mínimo 150x150px).',
    )

    # auth
    email = models.EmailField(u'e-mail', max_length=128, unique=True)

    created_at = models.DateTimeField(default=now)

    birth_date = models.DateField(u'data de aniversário', null=True, blank=True)
    starting_date = models.DateField(u'data de admissão', null=True, blank=True)
    leaving_date = models.DateField(u'data de demissão', null=True, blank=True)

    tags = TaggableManager(verbose_name=u'tags')

    objects = ActiveUserManager()
    all_objects = models.Manager()

    class MPTTMeta:
        parent_attr = 'reports_to'
        order_insertion_by = ['name']

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name or self.email

    def delete(self, *args, **kwargs):
        """
        Soft delete will not work due to MPTT implementation.
        Set `leaving_date` to a valid date and the account will not
        appear anymore.
        """
        raise Exception('An account cannot be deleted, set `leaving_date` instead')

    def is_staff(self):
        return self.is_staff

    def has_filled_profile(self):
        for attr in ('github_username', 'branch', 'phone', 'image'):
            if not getattr(self, attr):
                return False
        return True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_contrib_period(self):
        return relativedelta.relativedelta(
            self.leaving_date or now().date(),
            self.starting_date
        )
