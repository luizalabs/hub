from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.TeamListView.as_view(), name='team_list'),
    url(r'^(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^(?P<pk>\d+)/update/$', views.TeamUpdateView.as_view(), name='team_update'),
    url(r'^add/$', views.TeamCreateView.as_view(), name='team_create'),
)
