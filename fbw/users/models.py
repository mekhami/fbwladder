from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ladder.models import Match


@python_2_unicode_compatible
class User(AbstractUser):
    RACE_CHOICES = (
        ('Z', 'Zerg'),
        ('T', 'Terran'),
        ('P', 'Protoss'),
        ('R', 'Random'),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    battlenet = models.CharField(max_length=100, unique=True, null=True, blank=True)
    iccup = models.CharField(max_length=100, unique=True, null=True, blank=True)
    race = models.CharField(max_length=1, choices=RACE_CHOICES)
    rating = models.IntegerField(default=1200)
    shield_battery = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def games_played(self):
        return Match.objects.filter(Q(winner=self) | Q(loser=self)).count()
    

    @property
    def winrates(self):
        wins = Match.objects.filter(winner=self)
        losses = Match.objects.filter(loser=self)

        matchups = {
            'ZvT_wins': 0,
            'ZvT_games': 0,
            'ZvP_wins': 0,
            'ZvP_games': 0,
            'ZvZ_wins': 0,
            'ZvZ_games': 0,
            'TvZ_wins': 0,
            'TvZ_games': 0,
            'TvT_wins': 0,
            'TvT_games': 0,
            'TvP_wins': 0,
            'TvP_games': 0,
            'PvZ_wins': 0,
            'PvZ_games': 0,
            'PvP_wins': 0,
            'PvP_games': 0,
            'PvT_wins': 0,
            'PvT_games': 0,
        }

        # god forgive me for what i'm about to do
        for match in wins:
            if match.winner_race == 'Z':
                if match.loser_race == 'T':
                    matchups['ZvT_games'] += 1
                    matchups['ZvT_wins'] += 1
                if match.loser_race == 'P':
                    matchups['ZvP_games'] += 1
                    matchups['ZvP_wins'] += 1
                if match.loser_race == 'Z':
                    matchups['ZvZ_games'] += 1
                    matchups['ZvZ_wins'] += 1
            if match.winner_race == 'P':
                if match.loser_race == 'T':
                    matchups['PvT_games'] += 1
                    matchups['PvT_wins'] += 1
                if match.loser_race == 'P':
                    matchups['PvP_games'] += 1
                    matchups['PvP_wins'] += 1
                if match.loser_race == 'Z':
                    matchups['PvZ_games'] += 1
                    matchups['PvZ_wins'] += 1
            if match.winner_race == 'T':
                if match.loser_race == 'T':
                    matchups['TvT_games'] += 1
                    matchups['TvT_wins'] += 1
                if match.loser_race == 'P':
                    matchups['TvP_games'] += 1
                    matchups['TvP_wins'] += 1
                if match.loser_race == 'Z':
                    matchups['TvZ_games'] += 1
                    matchups['TvZ_wins'] += 1

        for match in losses:
            if match.loser_race == 'Z':
                if match.winner_race == 'T':
                    matchups['ZvT_games'] += 1
                if match.winner_race == 'P':
                    matchups['ZvP_games'] += 1
                if match.winner_race == 'Z':
                    matchups['ZvZ_games'] += 1
            if match.loser_race == 'P':
                if match.winner_race == 'T':
                    matchups['PvT_games'] += 1
                if match.winner_race == 'P':
                    matchups['PvP_games'] += 1
                if match.winner_race == 'Z':
                    matchups['PvZ_games'] += 1
            if match.loser_race == 'T':
                if match.winner_race == 'T':
                    matchups['TvT_games'] += 1
                if match.winner_race == 'P':
                    matchups['TvP_games'] += 1
                if match.winner_race == 'Z':
                    matchups['TvZ_games'] += 1

        return {
            'ZvT': "{0:.0f}%".format(matchups['ZvT_wins'] / matchups['ZvT_games'] * 100) if matchups['ZvT_games'] > 0 else "",
            'ZvP': "{0:.0f}%".format(matchups['ZvP_wins'] / matchups['ZvP_games'] * 100) if matchups['ZvP_games'] > 0 else "",
            'ZvZ': "{0:.0f}%".format(matchups['ZvZ_wins'] / matchups['ZvZ_games'] * 100) if matchups['ZvZ_games'] > 0 else "",
            'TvT': "{0:.0f}%".format(matchups['TvT_wins'] / matchups['TvT_games'] * 100) if matchups['TvT_games'] > 0 else "",
            'TvP': "{0:.0f}%".format(matchups['TvP_wins'] / matchups['TvP_games'] * 100) if matchups['TvP_games'] > 0 else "",
            'TvZ': "{0:.0f}%".format(matchups['TvZ_wins'] / matchups['TvZ_games'] * 100) if matchups['TvZ_games'] > 0 else "",
            'PvT': "{0:.0f}%".format(matchups['PvT_wins'] / matchups['PvT_games'] * 100) if matchups['PvT_games'] > 0 else "",
            'PvP': "{0:.0f}%".format(matchups['PvP_wins'] / matchups['PvP_games'] * 100) if matchups['PvP_games'] > 0 else "",
            'PvZ': "{0:.0f}%".format(matchups['PvZ_wins'] / matchups['PvZ_games'] * 100) if matchups['PvZ_games'] > 0 else "",
        }

    @property
    def unconfirmed_matches(self):
        unconfirmed_wins = Match.objects.filter(Q(winner=self) & Q(winner_confirmed=False)).count()
        unconfirmed_losses = Match.objects.filter(Q(loser=self) & Q(loser_confirmed=False)).count()
        return unconfirmed_wins + unconfirmed_losses
