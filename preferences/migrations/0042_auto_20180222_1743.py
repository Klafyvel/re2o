# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-22 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0041_merge_20180130_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optionaluser',
            name='all_can_create',
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='all_can_create_adherent',
            field=models.BooleanField(default=False, help_text="Les users peuvent créer d'autres adhérents"),
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='all_can_create_club',
            field=models.BooleanField(default=False, help_text='Les users peuvent créer un club'),
        ),
    ]