# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-23 01:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topologie', '0052_transferports'),
    ]



    operations = [
        migrations.DeleteModel(
        name='Switch',
        ),
        migrations.RenameModel(
        old_name='NewSw',
        new_name='Switch',
        ),
    ]
