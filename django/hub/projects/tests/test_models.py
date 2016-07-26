# coding: utf-8

import pytest

from factories import ProjectFactory
from projects.models import Project


@pytest.mark.django_db
class TestProjectModel(object):

    def test_model_unicode(self):
        project = ProjectFactory.create()
        assert project.name == unicode(project)

    def test_delete_mess(self, account):
        projects = ProjectFactory.create_batch(5, team__area__leader=account)

        assert 5 == Project.objects.count()

        projects[0].delete()

        assert 4 == Project.objects.count()
