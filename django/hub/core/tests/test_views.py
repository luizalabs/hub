# coding: utf-8

import json
import pytest

from django.shortcuts import resolve_url

from accounts.tests.factories import AccountFactory
from projects.tests.factories import ProjectFactory


def tags_url(tag_id):
    return resolve_url('core:tags_list', tag_id=tag_id)


class TagsTestMixin(object):
    @pytest.fixture(autouse=True)
    def setUp(self):
        AccountFactory.create(tags=('python',))
        ProjectFactory.create_batch(2, tags=('python', 'golang'))


@pytest.mark.django_db
class TestTagsListView(TagsTestMixin):
    python = 1
    golang = 2

    def test_get(self, logged_client):
        response = logged_client.get(tags_url(tag_id=self.python))
        assert 200 == response.status_code

    def test_wrong_get(self, logged_client):
        response = logged_client.get(tags_url(tag_id=40404040))
        assert 200 == response.status_code

    def test_template(self, logged_client):
        response = logged_client.get(tags_url(tag_id=self.python))
        assert 'core/tags_list.html' == response.template_name[0]

    def test_context(self, logged_client):
        response = logged_client.get(tags_url(tag_id=self.python))

        accounts = response.context['accounts']
        projects = response.context['projects']

        assert 1 == len(accounts)
        assert 2 == len(projects)

    def test_amount_of_returned_elements(self, logged_client):
        response = logged_client.get(tags_url(tag_id=self.golang))

        accounts = len(response.context['accounts'])
        projects = len(response.context['projects'])

        assert 2 == accounts + projects


@pytest.mark.django_db
class TestTagsJsonView(TagsTestMixin):
    tags_url = resolve_url('core:get_tags_json')

    @pytest.fixture
    def tags_response(self, logged_client):
        return logged_client.get(
            self.tags_url,
            HTTP_REFERER='localhost',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_get(self, tags_response):
        assert 200 == tags_response.status_code

    def test_json_returned(self, tags_response):
        expected = [
            {u'url': u'/tags/1/', u'tag': u'python', u'weight': 3},
            {u'url': u'/tags/2/', u'tag': u'golang', u'weight': 2}
        ]

        json_response = json.loads(tags_response.content)
        assert expected == json_response
