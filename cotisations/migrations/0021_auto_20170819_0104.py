# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cotisations", "0020_auto_20170819_0057")]

    operations = [
        migrations.AlterField(
            model_name="paiement",
            name="type_paiement",
            field=models.IntegerField(choices=[(0, "Autre"), (1, "Chèque")], default=0),
        )
    ]
