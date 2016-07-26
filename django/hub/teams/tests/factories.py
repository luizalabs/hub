# coding: utf-8

import factory
import pytest

from accounts.tests.factories import AccountFactory

from teams.models import Area, Team

__all__ = ['team', 'TeamFactory']


@pytest.fixture
def team():
    return TeamFactory.create()


class AreaFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Area

    leader = factory.SubFactory(AccountFactory)
    name = u'E-commerce'


class TeamFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Team

    area = factory.SubFactory(AreaFactory)
    leader = factory.SubFactory(AccountFactory)
    name = u'Big Data'
