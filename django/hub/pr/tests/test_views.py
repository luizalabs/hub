# coding: utf-8

from django.shortcuts import resolve_url

import pytest

from pr.models import PressRelease


def login(client, account):
    password = '_'
    account.set_password(password)
    account.save()

    client.login(username=account.email, password=password)


@pytest.fixture
def press_release_url(press_release):
    return resolve_url('pr:pressrelease_update', pk=press_release.id)


@pytest.mark.django_db
class TestPrUpdateView(object):

    def test_view_returns_when_user_isnt_press_release_owner(self,
                                                             account,
                                                             client,
                                                             press_release,
                                                             press_release_url):
        """ View can be accessed only by press release owner or superuser """
        login(client, account)
        response = client.get(press_release_url)
        assert 403 == response.status_code

    def test_view_returns_200_for_press_release_owner(self,
                                                      client,
                                                      press_release,
                                                      press_release_url):
        login(client, press_release.added_by)
        response = client.get(press_release_url)
        assert 200 == response.status_code

    def test_post_view_updates_press_release(self,
                                             client,
                                             press_release,
                                             press_release_url,
                                             team):
        assert 0 == press_release.teams.count()

        post_data = {
            'title': 'Novo',
            'author_name': 'Novo autor',
            'author_email': 'autor@email.com',
            'text': 'Novo texto',
            'teams': team.id
        }

        login(client, press_release.added_by)
        client.post(press_release_url, data=post_data)

        refreshed_press_release = PressRelease.objects.get(id=press_release.id)

        assert 'Novo' == refreshed_press_release.title
        assert 'Novo autor' == refreshed_press_release.author_name
        assert 'autor@email.com' == refreshed_press_release.author_email
        assert 'Novo texto' == refreshed_press_release.text

        assert 1 == refreshed_press_release.teams.count()
