from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .models import Match
from .forms import MatchForm
from fbw.users.models import User


# Create your views here.
class MatchFormView(generic.FormView):
    form_class = MatchForm
    template_name = 'ladder/submit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user == self.object.winner:
            self.object.winner_confirmed = True
        elif self.request.user == self.object.loser:
            self.object.loser_confirmed = True
        self.object.save()
        return super().form_valid(form)


class MatchDetailView(generic.DetailView):
    model = Match
    template_name = 'ladder/match_detail.html'


class UnconfirmedMatchesView(generic.ListView):
    model = Match
    template_name = 'ladder/unconfirmed_matches.html'
    context_object_name = 'matches'
    paginate_by = 10

    def get_queryset(self):
        unconfirmed_wins = Match.objects.filter(Q(winner=self.request.user) & Q(winner_confirmed=False))
        unconfirmed_losses = Match.objects.filter(Q(loser=self.request.user) & Q(loser_confirmed=False))
        return unconfirmed_wins | unconfirmed_losses

class PlayerListView(generic.ListView):
    model = User
    template_name = 'ladder/player_list.html'
    context_object_name = 'players'
    ordering = '-rating'
    paginate_by = 15


class MatchListView(generic.ListView):
    model = Match
    template_name = 'ladder/match_list.html'
    context_object_name = 'matches'
    paginate_by = 15
    queryset = Match.objects.all().prefetch_related('winner', 'loser')


class IndexView(generic.ListView):
    model = User
    template_name = 'ladder/match_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_list'] = User.objects.all().order_by('-rating')[:10]
        context['recent_matches'] = Match.objects.all().prefetch_related('winner', 'loser')[:10]
        return context


def confirm_match(request, pk):
    match = Match.objects.get(pk=pk)
    if request.user == match.winner:
        match.winner_confirmed = True
        match.save()
        return redirect(match)
    elif request.user == match.loser:
        match.loser_confirmed = True
        match.save()
        return redirect(match)
    else:
        return HttpResponseForbidden()
