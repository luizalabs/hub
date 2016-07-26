from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from news.models import Entry


admin.autodiscover()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['news_entries'] = Entry.objects.order_by('-created_at')
        return context


class ProjectsRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return '/products/{}'.format(self.kwargs.get('pattern', ''))


urlpatterns = patterns(
    '',
    url('^$', HomeView.as_view(), name='home'),
    url(r'^login/$', TemplateView.as_view(template_name='login.html')),
    url(r'^mgr/', include(admin.site.urls)),
    url(r'^projects/(?P<pattern>.*?)$', ProjectsRedirectView.as_view()),

    # third party
    (r'^accounts/', include('allauth.urls')),

    # local apps
    (r'^pr/', include('pr.urls', namespace='pr')),
    (r'^people/', include('accounts.urls', namespace='accounts')),
    (r'^teams/', include('teams.urls', namespace='teams')),
    (r'^products/', include('projects.urls', namespace='projects')),
    (r'^', include('core.urls', namespace='core')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
