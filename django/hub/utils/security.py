# coding: utf-8
import re

from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url as r


def ajax_basic_protection(func):
    def wrapper(request, *args, **kwargs):
        origin = request.META.get('HTTP_REFERER', '')
        regex = r"(.*luizalabs.*|.*localhost.*|.*127.0.*)"
        match = re.match(regex, origin)
        if not request.is_ajax() or not match:
            return HttpResponseRedirect(r('home'))

        return func(request, *args, **kwargs)
    return wrapper
