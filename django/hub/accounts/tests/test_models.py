# coding: utf-8

import pytest

from django.utils.timezone import now

from accounts.models import Account
from accounts.tests.factories import AccountFactory


@pytest.mark.django_db
class TestAccount(object):

    def test_model_unicode(self, account):
        assert unicode(account) == account.name

    def test_get_short_name(self, account):
        assert account.get_short_name() == account.name

    def test_get_full_name(self, account):
        assert account.get_full_name() == account.name

    def test_reports_to_fk(self, account):
        dependent = AccountFactory.create(reports_to=account)

        assert account.reports_to is None
        assert dependent.reports_to == account

    def test_inactive_account(self, account):
        assert Account.objects.count() == 1

        account.leaving_date = now()
        account.save()

        assert Account.objects.count() == 0

    def test_delete_should_raise_exception(self, account):
        with pytest.raises(Exception):
            account.delete()
