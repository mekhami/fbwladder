# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 18:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170526_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='discord',
        ),
    ]