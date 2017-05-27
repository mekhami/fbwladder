from django.conf.urls import url

from .views import IndexView, MatchFormView, MatchDetailView, confirm_match, PlayerListView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^submit/', MatchFormView.as_view(), name='submit'),
    url(r'^match/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match-detail'),
    url(r'^match/(?P<pk>\d+)/confirm$', confirm_match, name='match-confirm'),
    url(r'^players$', PlayerListView.as_view(), name='player-list'),
]
