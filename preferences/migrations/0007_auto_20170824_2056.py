# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0006_auto_20170824_0143")]

    operations = [
        migrations.AlterField(
            model_name="assooption",
            name="name",
            field=models.CharField(
                default="Association réseau de l'école machin", max_length=256
            ),
        )
    ]
