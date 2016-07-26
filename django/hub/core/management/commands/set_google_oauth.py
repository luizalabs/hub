#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    args = '<client_id> <client_secret>'
    help = 'Set Google Account OAuth2 support'

    def handle(self, *args, **options):
        try:
            client_id, client_secret = args
        except ValueError:
            raise CommandError(
                'Invalid arguments: {}.\nArgs should be: {}'.format(
                    args, Command.args))
        app, created = SocialApp.objects.get_or_create(
            provider='google', name='luizalabs')

        app.client_id = client_id
        app.secret = client_secret

        app.sites.add(Site.objects.get_current())
        app.save()
