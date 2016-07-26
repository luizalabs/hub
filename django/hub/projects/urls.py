from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.ProjectListView.as_view(), name='project_list'),
    url(r'^add/$', views.ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<project_pk>\d+)/applications/add/$',
        views.ProjectCreateView.as_view(),
        name='child_project_create'),
    url(r'^(?P<pk>\d+)/$',
        views.ProjectDetailView.as_view(),
        name='project_detail'),
    url(
        r'^(?P<pk>\d+)/update/$',
        views.ProjectUpdateView.as_view(),
        name='project_update'
    ),
    url(
        r'^(?P<project_id>\d+)/changelog/add/$',
        views.ChangelogCreateView.as_view(),
        name='changelog_add'
    ),
    url(
        r'^changelog/(?P<changelog_id>\d+)/update/$',
        views.ChangelogUpdateView.as_view(),
        name='changelog_update'
    ),
    url(
        r'^changelog/(?P<changelog_id>\d+)/delete/$',
        views.ChangelogDeleteView.as_view(),
        name='changelog_delete'
    ),
    url(
        r'^changelog/(?P<changelog_id>\d+)/send_mail/$',
        views.ChangelogSendMailView.as_view(),
        name='changelog_send_mail'
    ),
    url(
        r'^changelog/(?P<changelog_id>\d+)/send_slack/$',
        views.ChangelogSendSlackView.as_view(),
        name='changelog_send_slack'
    ),
)
