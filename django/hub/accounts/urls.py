from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.AccountListView.as_view(), name='account_list'),
    url(
        r'^organogram/$',
        views.OrganogramView.as_view(),
        name='organogram'
    ),
    url(
        r'^(?P<slug>.*)/update/$',
        views.AccountUpdateView.as_view(),
        name='account_update'
    ),
    url(
        r'^(?P<slug>.*)/add-award/$',
        views.AccountAwardCreateView.as_view(),
        name='account_award_add'
    ),
    url(
        r'^(?P<slug>.*)/$',
        views.AccountDetailView.as_view(),
        name='account_detail'
    )
)
