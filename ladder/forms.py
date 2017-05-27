from django import forms

from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ('date', 'winner_confirmed', 'loser_confirmed', 'calculated', 'winner_rating_change', 'loser_rating_change')
