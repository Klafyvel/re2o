# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-01-02 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topologie', '0067_auto_20181230_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelswitch',
            name='is_itself_module',
            field=models.BooleanField(default=False, help_text='Is the switch, itself, considered as a module'),
        ),
    ]
