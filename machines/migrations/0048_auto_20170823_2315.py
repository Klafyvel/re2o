# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-23 21:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("machines", "0047_auto_20170809_0606")]

    operations = [
        migrations.AlterField(
            model_name="iptype",
            name="domaine_range",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(16),
                    django.core.validators.MaxValueValidator(32),
                ]
            ),
        )
    ]
