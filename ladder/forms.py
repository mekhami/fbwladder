from django import forms

from .models import Match, Report

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ('replay', 'date', 'winner_confirmed', 'loser_confirmed', 'calculated', 'winner_rating_change', 'loser_rating_change')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 'description')

    def __init__(self, *args, **kwargs):
        self.match_id = kwargs.pop('match_id', None)
        self.reporter = kwargs.pop('reporter')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        model = super().save(commit=False)
        model.match = Match.objects.get(pk=self.match_id)
        model.reporter = self.reporter

        if commit:
            model.save()
        return model


class MatchReplayForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('replay',)
