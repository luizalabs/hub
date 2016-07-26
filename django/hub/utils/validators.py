# coding: utf-8

from django.core.validators import validate_email


def validate_email_list(emails_string):
    emails = [e.strip() for e in emails_string.split(',')]

    for email in emails:
        validate_email(email)
