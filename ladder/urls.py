from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submit/', views.MatchFormView.as_view(), name='submit'),
    url(r'^match/$', views.MatchListView.as_view(), name='match-list'),
    url(r'^match/unconfirmed$', views.UnconfirmedMatchesView.as_view(), name='unconfirmed-matches'),
    url(r'^match/(?P<pk>\d+)/$', views.MatchDetailView.as_view(), name='match-detail'),
    url(r'^match/(?P<pk>\d+)/confirm$', views.confirm_match, name='match-confirm'),
    url(r'^match/(?P<pk>\d+)/report$', views.MatchReportView.as_view(), name='match-report'),
    url(r'^players$', views.PlayerListView.as_view(), name='player-list'),
]
