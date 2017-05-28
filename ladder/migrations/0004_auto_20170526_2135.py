# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0003_auto_20170526_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='calculated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_map',
            field=models.CharField(choices=[('FS', 'Fighting Spirit'), ('CB', 'Circuit Breaker'), ('DE', 'Destination'), ('JA', 'Jade'), ('QB', 'Queensbridge')], max_length=3),
        ),
    ]