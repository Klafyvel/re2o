# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-05 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("machines", "0053_text")]

    operations = [
        migrations.AddField(
            model_name="text",
            name="zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="machines.Extension"
            ),
            preserve_default=False,
        )
    ]
