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
