# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-14 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0033_generaloption_gtu_sum_up")]

    operations = [
        migrations.AddField(
            model_name="generaloption",
            name="GTU",
            field=models.FileField(default="", upload_to="GTU"),
        ),
        migrations.AlterField(
            model_name="generaloption",
            name="GTU_sum_up",
            field=models.TextField(blank=True, default=""),
        ),
    ]
