# coding: utf-8

import pytest


@pytest.mark.django_db
def test_press_release_unicode(press_release):
    assert press_release.title == unicode(press_release)
