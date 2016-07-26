# coding: utf-8

import factory
import pytest

from accounts.tests.factories import AccountFactory
from pr.models import PressRelease


__all__ = ['press_release', 'PressReleaseFactory']


@pytest.fixture
def press_release():
    return PressReleaseFactory.create()


class PressReleaseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = PressRelease

    title = factory.Sequence(lambda n: u'Release número {0}'.format(n))
    author_name = u'Descrição'
    author_email = u'renato@email.com'
    added_by = factory.SubFactory(AccountFactory)
