from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url('^$', views.PressReleaseListView.as_view(), name='pressrelease_list'),
    url(
        '^(?P<pk>\d+)/$',
        views.PressReleaseDetailView.as_view(),
        name='pressrelease_detail'
    ),
    url(
        '^(?P<pk>\d+)/update/$',
        views.PressReleaseUpdateView.as_view(),
        name='pressrelease_update'
    ),
    url(
        '^(?P<pressrelease_id>\d+)/faq/add/$',
        views.QuestionCreateView.as_view(),
        name='pressrelease_question_add'
    ),
    url(
        '^(?P<pressrelease_id>\d+)/faq/(?P<pk>\d+)/$',
        views.QuestionUpdateView.as_view(),
        name='pressrelease_question_update'
    ),
    url(
        '^add/$',
        views.PressReleaseCreateView.as_view(),
        name='pressrelease_add'
    ),
)
