# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-26 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0012_generaloption_req_expire_hrs")]

    operations = [
        migrations.AddField(
            model_name="generaloption",
            name="site_name",
            field=models.CharField(default="Re2o", max_length=32),
        )
    ]
