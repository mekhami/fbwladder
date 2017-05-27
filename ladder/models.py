import math

from django.db import models
from django.conf import settings
from django.urls import reverse


class Match(models.Model):
    LEAGUE_MAPS = (
        ('FS', 'Fighting Spirit'),
        ('CB', 'Circuit Breaker'),
        ('DE', 'Destination'),
        ('JA', 'Jade'),
        ('QB', 'Queensbridge'),
    )

    calculated = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    match_map = models.CharField('Map', max_length=3, choices=LEAGUE_MAPS)
    rated = models.BooleanField(default=True)
    replay = models.FileField(upload_to='replays')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='win')
    winner_confirmed = models.BooleanField(default=False)
    winner_rating_change = models.IntegerField(null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loss')
    loser_confirmed = models.BooleanField(default=False)
    loser_rating_change = models.IntegerField(null=True)

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

    @staticmethod
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

        if new_loser_rating < 1:
            loser.rating = 1

        return (winner.rating, loser.rating)
