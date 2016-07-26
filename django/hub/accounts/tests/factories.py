# coding: utf8

import factory
import pytest

from accounts.models import Account

__all__ = ['account', 'AccountFactory']


@pytest.fixture
def account():
    return AccountFactory.create()


class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Account

    name = factory.Sequence(lambda n: 'Test {}'.format(n))
    email = factory.Sequence(lambda n: 'e{}@luizalabs.com'.format(n))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
