import json
import math
import os
import requests
import subprocess
import tempfile

from django.db import models
from django.db.models import Q
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
    RACE_CHOICES = (
        ('Z', 'Zerg'),
        ('T', 'Terran'),
        ('P', 'Protoss'),
        ('R', 'Random'),
    )

    calculated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    match_map = models.CharField('Map', max_length=100, null=True, blank=True)
    replay = models.FileField(upload_to='replays')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='win', null=True)
    winner_confirmed = models.BooleanField(default=False)
    winner_race = models.CharField(max_length=1, choices=RACE_CHOICES, null=True, blank=True)
    winner_rating_change = models.IntegerField(null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loss', null=True)
    loser_confirmed = models.BooleanField(default=False)
    loser_race = models.CharField(max_length=1, choices=RACE_CHOICES, null=True, blank=True)
    loser_rating_change = models.IntegerField(null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.winner.username + ' vs ' + self.loser.username + ' ' + self.date.strftime('%m/%d/%y')

    def parse_replay(self, race=True, users=True, match_map=True):
        from fbw.users.models import User  # noqa

        replay_content = requests.get(self.replay.url).content
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(replay_content)
        screp_path = os.path.join(os.path.dirname(__file__)) + '/screp'
        parsed_map = json.loads(
           subprocess.run([screp_path, "-map", tmp.name], stdout=subprocess.PIPE).stdout.decode('utf-8')
        )
        parsed_cmds = json.loads(
           subprocess.run([screp_path, "-cmds", tmp.name], stdout=subprocess.PIPE).stdout.decode('utf-8')
        )

        if match_map:
            self.match_map = parsed_map["Header"]["Map"]

        found = False
        for cmd in reversed(parsed_cmds["Commands"]["Cmds"]):
            try:
                if cmd["Reason"]["Name"] == "Defeat":
                    defeat_command = cmd
                    found = True
                    break
            except KeyError:
                pass

        if not found:
            return

        loser_id = defeat_command["PlayerID"]  # will be 1 or 0 for all two player games
        winner_id = int(not loser_id)  # quite pretty, gets the opposite of loser_id

        try:
            winner = next(d for d in parsed_map["Header"]["Players"] if d['ID'] == winner_id)
            loser = next(d for d in parsed_map["Header"]["Players"] if d['ID'] == loser_id)
        except StopIteration:
            return

        if race:
            self.winner_race = winner["Race"]["Name"][0]
            self.loser_race = loser["Race"]["Name"][0]

        if users:
            try:
                self.winner = User.objects.get(
                    Q(iccup=winner["Name"]) | 
                    Q(battlenet=winner["Name"]) | 
                    Q(shield_battery=winner["Name"])
                )
            except User.DoesNotExist:
                pass
            try:
                self.loser = User.objects.get(
                    Q(iccup=loser["Name"]) | 
                    Q(battlenet=loser["Name"]) | 
                    Q(shield_battery=loser["Name"])
                )
            except User.DoesNotExist:
                pass

        tmp.close()

    def save(self, *args, **kwargs):
        if not self.pk:  # row init
            super().save(*args, **kwargs)
            self.parse_replay()
        if self.winner_confirmed and self.loser_confirmed and not self.calculated:
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
