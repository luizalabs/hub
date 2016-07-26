# coding: utf-8

import factory

from accounts.tests.factories import AccountFactory
from projects.models import Project, Changelog
from teams.tests.factories import TeamFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Project

    name = factory.Sequence(lambda n: u'Projeto {0}'.format(n))
    description = u'Descrição'
    added_by = factory.SubFactory(AccountFactory)
    team = factory.SubFactory(TeamFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class ChangelogFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Changelog

    description = factory.Sequence(lambda n: u'Versão 0.{}'.format(n))
    project = factory.SubFactory(ProjectFactory)
    added_by = factory.SubFactory(AccountFactory)
