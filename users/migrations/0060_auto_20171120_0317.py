# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-20 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0059_auto_20171025_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='administrators',
            field=models.ManyToManyField(blank=True, related_name='club_administrator', to='users.Adherent'),
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='club_members', to='users.Adherent'),
        ),
    ]
