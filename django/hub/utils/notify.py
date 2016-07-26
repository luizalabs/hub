# coding: utf-8

import json

from django.conf import settings

from slackclient import SlackClient


sc = SlackClient(settings.CHANGELOG_API_TOKEN)


def slack(**kwargs):
    data = sc.api_call("chat.postMessage", **kwargs)
    data = {'timestamp': data.get('ts'), 'channel': data.get('channel')}
    return json.dumps(data)
