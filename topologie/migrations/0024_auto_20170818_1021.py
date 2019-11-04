# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("topologie", "0023_auto_20170817_1654")]

    operations = [
        migrations.AlterField(
            model_name="switch",
            name="stack",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="topologie.Stack",
            ),
        )
    ]
