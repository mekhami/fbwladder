from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submit/', login_required(views.MatchFormView.as_view()), name='submit'),
    url(r'^match/$', login_required(views.MatchListView.as_view()), name='match-list'),
    url(r'^match/unconfirmed$', login_required(views.UnconfirmedMatchesView.as_view()), name='unconfirmed-matches'),
    url(r'^match/(?P<pk>\d+)/$', login_required(views.MatchDetailView.as_view()), name='match-detail'),
    url(r'^match/(?P<pk>\d+)/confirm$', login_required(views.confirm_match), name='match-confirm'),
    url(r'^match/(?P<pk>\d+)/report$', login_required(views.MatchReportView.as_view()), name='match-report'),
    url(r'^players$', views.PlayerListView.as_view(), name='player-list'),
]
