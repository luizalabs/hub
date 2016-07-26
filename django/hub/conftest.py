import pytest


from accounts.tests.factories import *
from pr.tests.factories import *
from teams.tests.factories import *


@pytest.fixture
def logged_client(client):
    account, password = AccountFactory.create(__sequence=0), '_'
    account.set_password(password)
    account.save()

    client.login(username=account.email, password=password)
    return client
