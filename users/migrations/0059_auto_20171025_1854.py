# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-25 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0058_auto_20171025_0154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adherent',
            old_name='room_adherent',
            new_name='room',
        ),
        migrations.RenameField(
            model_name='club',
            old_name='room_club',
            new_name='room',
        ),
    ]
