# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-07-12 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0059_auto_20190120_1739")]

    operations = [
        migrations.AlterField(
            model_name="reminder",
            name="message",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Message displayed specifically for this reminder",
                null=True,
            ),
        )
    ]
