# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-08-31 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cotisations", "0033_auto_20180818_1319")]

    operations = [
        migrations.AlterField(
            model_name="facture",
            name="valid",
            field=models.BooleanField(default=False, verbose_name="validated"),
        )
    ]
