# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-28 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0042_auto_20180222_1743")]

    operations = [
        migrations.AddField(
            model_name="optionalmachine",
            name="create_machine",
            field=models.BooleanField(
                default=True, help_text="Permet à l'user de créer une machine"
            ),
        )
    ]
