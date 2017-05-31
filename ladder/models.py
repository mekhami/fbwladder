import math
import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse


def assign_elo_changes(winner, loser):
    win_rating = winner.rating
    lose_rating = loser.rating
    difference = win_rating - lose_rating
    exp = (difference * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))

    if win_rating < 2100:
        k = 32
    elif win_rating >= 2100 and win_rating < 2400:
        k = 24
    else:
        k = 16

    winner.rating = round(win_rating + (k * (1 - odds)))
    new_rank_diff = winner.rating - win_rating
    loser.rating = lose_rating - new_rank_diff

    if loser.rating < 1:
        loser.rating = 1

    return (winner.rating, loser.rating)


def replay_file_name(instance, filename):
    name, file_ext = os.path.splitext(filename)
    return 'replays/{}-{}-{}{}'.format(
        instance.winner.username, 
        instance.loser.username, 
        instance.date.strftime('%m-%d-%y'), 
        file_ext
    )

class Match(models.Model):
    LEAGUE_MAPS = (
        ('AN', 'Andromeda'),
        ('AV', 'Avalon'),
        ('AZ', 'Aztec'),
        ('BW', 'Beltway'),
        ('BZ', 'Benzene'),
        ('BR', 'Bloody Ridge'),
        ('BS', 'Blue Storm'),
        ('CR', 'Chain Reaction'),
        ('CB', 'Circuit Breaker'),
        ('CO', 'Colosseum'),
        ('CG', 'Cross Game'),
        ('DP', 'Dante\'s Peak'),
        ('DE', 'Demian'),
        ('DT', 'Desertec'),
        ('DS', 'Destination'),
        ('ED', 'Eddy'),
        ('EC', 'Electric Circuit'),
        ('EM', 'Empire of the Sun'),
        ('ES', 'Eye of the Storm'),
        ('FS', 'Fighting Spirit'),
        ('FO', 'Fortress'),
        ('GL', 'Gemlong'),
        ('GR', 'Grandline'),
        ('GZ', 'Ground Zero'),
        ('HB', 'Heartbeat'),
        ('HR', 'Heartbreak Ridge'),
        ('HU', 'Hunters'),
        ('IC', 'Icarus'),
        ('JA', 'Jade'),
        ('LM', 'La Mancha'),
        ('LQ', 'Latin Quarter'),
        ('LO', 'Longinus'),
        ('LU', 'Luna'),
        ('MP', 'Match Point'),
        ('ME', 'Medusa'),
        ('MI', 'Mist'),
        ('OT', 'Othello'),
        ('OS', 'Outsider'),
        ('OW', 'Overwatch'),
        ('PF', 'Pathfinder'),
        ('PR', 'Polaris Rhapsody'),
        ('PY', 'Python'),
        ('QB', 'Queensbridge'),
        ('RE', 'Resonance'),
        ('RK', 'Roadkill'),
        ('SR', 'Sniper Ridge'),
        ('TC', 'Tau Cross'),
        ('TS', 'Toad Stone'),
        ('TO', 'Tornado'),
        ('WC', 'Wind and Cloud')
    )

    calculated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    match_map = models.CharField('Map', max_length=3, choices=LEAGUE_MAPS)
    rated = models.BooleanField(default=True)
    replay = models.FileField(upload_to='replays')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='win')
    winner_confirmed = models.BooleanField(default=False)
    winner_rating_change = models.IntegerField(null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loss')
    loser_confirmed = models.BooleanField(default=False)
    loser_rating_change = models.IntegerField(null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.winner.username + ' vs ' + self.loser.username + ' ' + self.date.strftime('%m/%d/%y')

    def save(self, *args, **kwargs):
        if self.winner_confirmed and self.loser_confirmed and self.rated:
            winner_pre = self.winner.rating
            loser_pre = self.loser.rating
            new_winner, new_loser = assign_elo_changes(self.winner, self.loser)
            self.winner_rating_change = new_winner - winner_pre
            self.loser_rating_change = loser_pre - new_loser

            self.calculated = True

            self.winner.rating = new_winner
            self.winner.save()

            self.loser.rating = new_loser
            self.loser.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ladder:match-detail', args=[str(self.id)])


class Report(models.Model):
    REPORT_TYPES = (
        ('FRAUD', 'Fraudulent Match'),
        ('BM', 'BM/Misconduct'),
        ('DUP', 'Duplicate Match'),
        ('INC', 'Incorrect Data')
    )

    description = models.TextField()
    time_reported = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL)
    resolved = models.BooleanField(default=False)
    match = models.ForeignKey(Match)

    def __str__(self):
        return '{} - {} vs {}'.format(
            self.report_type,
            self.match.winner.username,
            self.match.loser.username
        )


@receiver(pre_delete, sender=Match)
def revert_rating(sender, instance, **kwargs):
    if instance.calculated:
        instance.winner.rating -= instance.winner_rating_change
        instance.loser.rating += instance.loser_rating_change
        instance.winner.save()
        instance.loser.save()
