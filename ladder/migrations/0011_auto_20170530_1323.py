# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-30 13:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0010_auto_20170529_0016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ('-date',)},
        ),
    ]
