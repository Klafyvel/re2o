# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-05-25 20:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("machines", "0081_auto_20180521_1413")]

    operations = [
        migrations.AlterModelOptions(
            name="service_link",
            options={
                "permissions": (
                    ("view_service_link", "Peut voir un objet service_link"),
                )
            },
        )
    ]
