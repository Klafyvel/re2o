# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-26 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("topologie", "0023_auto_20170826_1530")]

    operations = [
        migrations.AlterField(
            model_name="port",
            name="radius",
            field=models.CharField(
                choices=[
                    ("NO", "NO"),
                    ("STRICT", "STRICT"),
                    ("BLOQ", "BLOQ"),
                    ("COMMON", "COMMON"),
                ],
                default="NO",
                max_length=32,
            ),
        )
    ]
