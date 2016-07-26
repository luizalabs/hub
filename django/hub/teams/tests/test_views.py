# coding: utf - 8

import pytest

from django.shortcuts import resolve_url

from factories import TeamFactory


@pytest.mark.django_db
class TestTeamViews(object):
    team_list_url = resolve_url('teams:team_list')

    @pytest.fixture
    def teams(self):
        return TeamFactory.create_batch(5)

    @pytest.fixture
    def team_view_response(self, logged_client):
        response = logged_client.get(self.team_list_url)
        return response

    def test_ping(self, team_view_response):
        assert 200 == team_view_response.status_code

    def test_team_list(self, teams, team_view_response):

        for team in teams:
            assert str(team.name) in team_view_response.content
