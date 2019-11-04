# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-18 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("machines", "0061_auto_20171015_2033")]

    operations = [
        migrations.AddField(
            model_name="extension",
            name="origin_v6",
            field=models.GenericIPAddressField(blank=True, null=True, protocol="IPv6"),
        )
    ]
