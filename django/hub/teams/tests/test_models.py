# coding: utf-8

import pytest


@pytest.mark.django_db
def test_team_model_unicode(team):
    team_unicode = u'{} - {}'.format(team.area.name, team.name)

    assert team_unicode == unicode(team)
