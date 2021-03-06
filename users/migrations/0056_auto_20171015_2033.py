# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-15 18:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [("users", "0055_auto_20171003_0556")]

    operations = [
        migrations.AlterField(
            model_name="listright",
            name="gid",
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="listright",
            name="listright",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-z]+$",
                        message="Les groupes unix ne peuvent contenir            que des lettres minuscules",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="rezo_rez_uid",
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="uid_number",
            field=models.PositiveIntegerField(
                default=users.models.get_fresh_user_uid, unique=True
            ),
        ),
    ]
