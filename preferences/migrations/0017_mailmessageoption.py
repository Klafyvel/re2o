# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-08 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("preferences", "0016_auto_20170902_1520")]

    operations = [
        migrations.CreateModel(
            name="MailMessageOption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("welcome_mail_fr", models.TextField(default="")),
                ("welcome_mail_en", models.TextField(default="")),
            ],
        )
    ]
