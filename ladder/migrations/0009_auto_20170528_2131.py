# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-28 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0008_auto_20170528_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_map',
            field=models.CharField(choices=[('AN', 'Andromeda'), ('AV', 'Avalon'), ('AZ', 'Aztec'), ('BW', 'Beltway'), ('BZ', 'Benzene'), ('BR', 'Bloody Ridge'), ('BS', 'Blue Storm'), ('CR', 'Chain Reaction'), ('CB', 'Circuit Breaker'), ('CO', 'Colosseum'), ('CG', 'Cross Game'), ('DP', "Dante's Peak"), ('DE', 'Demian'), ('DT', 'Desertec'), ('DS', 'Destination'), ('ED', 'Eddy'), ('EC', 'Electric Circuit'), ('EM', 'Empire of the Sun'), ('ES', 'Eye of the Storm'), ('FS', 'Fighting Spirit'), ('FO', 'Fortress'), ('GL', 'Gemlong'), ('GR', 'Grandline'), ('GZ', 'Ground Zero'), ('HB', 'Heartbeat'), ('HR', 'Heartbreak Ridge'), ('HU', 'Hunters'), ('IC', 'Icarus'), ('JA', 'Jade'), ('LM', 'La Mancha'), ('LQ', 'Latin Quarter'), ('LO', 'Longinus'), ('LU', 'Luna'), ('MP', 'Match Point'), ('ME', 'Medusa'), ('MI', 'Mist'), ('OT', 'Othello'), ('OS', 'Outsider'), ('OW', 'Overwatch'), ('PF', 'Pathfinder'), ('PR', 'Polaris Rhapsody'), ('PY', 'Python'), ('QB', 'Queensbridge'), ('RE', 'Resonance'), ('RK', 'Roadkill'), ('SR', 'Sniper Ridge'), ('TC', 'Tau Cross'), ('TS', 'Toad Stone'), ('TO', 'Tornado'), ('WC', 'Wind and Cloud')], max_length=3, verbose_name='Map'),
        ),
    ]
