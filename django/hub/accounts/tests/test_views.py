# coding: utf-8

import itertools
import pytest

from django.shortcuts import resolve_url

from factories import AccountFactory


@pytest.mark.django_db
class TestAccountViews(object):
    accounts_list_url = resolve_url('accounts:account_list')
    accounts_organogram_url = resolve_url('accounts:organogram')

    def account_detail_url(self, slug):
        return resolve_url('accounts:account_detail', slug=slug)

    def test_ping(self, logged_client):
        response = logged_client.get(self.accounts_list_url)
        assert 200 == response.status_code

    def test_account_list(self, logged_client, account):
        response = logged_client.get(self.accounts_list_url)
        assert account in response.context_data['account_list']

    def test_account_detail(self, logged_client, account):
        account_url = self.account_detail_url(account.email)

        response = logged_client.get(account_url)
        assert account == response.context_data['account']

    def test_organogram(self, logged_client):
        account_create = lambda r: AccountFactory.create(reports_to=r)

        accounts = AccountFactory.create_batch(5)
        subaccounts = map(account_create, accounts)
        subaccounts_2 = map(account_create, subaccounts)

        response = logged_client.get(self.accounts_organogram_url)

        for account in itertools.chain(accounts, subaccounts, subaccounts_2):
            assert account.name in response.content
