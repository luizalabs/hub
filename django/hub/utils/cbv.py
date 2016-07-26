# coding: utf-8
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse


class ProtectedMixin(object):
    login_required = True
    admin_required = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(),
                                     settings.LOGIN_URL, 'next')

        if self.admin_required and not request.user.is_superuser:
            return HttpResponse(u'User must be admin to access')

        return super(ProtectedMixin, self).dispatch(request, *args, **kwargs)
