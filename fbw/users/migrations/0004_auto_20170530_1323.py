# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-30 13:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_discord'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('name',)},
        ),
    ]
