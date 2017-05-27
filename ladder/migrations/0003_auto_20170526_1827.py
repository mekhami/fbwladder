# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 18:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0002_auto_20170526_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='win', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
