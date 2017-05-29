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

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def games_played(self):
        return Match.objects.filter(Q(winner=self) | Q(loser=self)).count()

    @property
    def vZ_winrate(self):
        wins = Match.objects.filter(Q(winner=self) & Q(loser__race='Z')).count()
        losses = Match.objects.filter(Q(loser=self) & Q(winner__race='Z')).count()
        if wins + losses == 0:
            return ""
        return "{0:.0f}%".format(wins / (wins+losses) * 100)

    @property
    def vT_winrate(self):
        wins = Match.objects.filter(Q(winner=self) & Q(loser__race='T')).count()
        losses = Match.objects.filter(Q(loser=self) & Q(winner__race='T')).count()
        if wins + losses == 0:
            return ""
        return "{0:.0f}%".format(wins / (wins+losses) * 100)

    @property
    def vP_winrate(self):
        wins = Match.objects.filter(Q(winner=self) & Q(loser__race='P')).count()
        losses = Match.objects.filter(Q(loser=self) & Q(winner__race='P')).count()
        if wins + losses == 0:
            return ""
        return "{0:.0f}%".format(wins / (wins+losses) * 100)

    @property
    def vR_winrate(self):
        wins = Match.objects.filter(Q(winner=self) & Q(loser__race='R')).count()
        losses = Match.objects.filter(Q(loser=self) & Q(winner__race='R')).count()
        if wins + losses == 0:
            return ""
        return "{0:.0f}%".format(wins / (wins+losses) * 100)
