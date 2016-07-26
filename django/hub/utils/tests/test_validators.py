# coding: utf-8

import pytest

from django.core.exceptions import ValidationError

from utils.validators import validate_email_list


def test_validate_with_invalid_email_raises_exception():
    with pytest.raises(ValidationError):
        validate_email_list('invalid, test@luizalabs.com')


def test_validate_with_valid_emails():
    validate_email_list('test@luizalabs.com, other@luizalabs.com')


def test_validate_with_missing_comma_raises_exception():
    with pytest.raises(ValidationError):
        validate_email_list('test@luizalabs.com,')
