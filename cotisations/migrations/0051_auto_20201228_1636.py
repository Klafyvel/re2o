# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-28 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cotisations", "0050_auto_20201102_2342"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="duration_connection",
            field=models.PositiveIntegerField(
                verbose_name="duration of the connection (in months)"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="duration_days_connection",
            field=models.PositiveIntegerField(
                verbose_name="duration of the connection (in days, will be added to duration in months)"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="duration_days_membership",
            field=models.PositiveIntegerField(
                verbose_name="duration of the membership (in days, will be added to duration in months)"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="duration_membership",
            field=models.PositiveIntegerField(
                verbose_name="duration of the membership (in months)"
            ),
        ),
        migrations.AlterField(
            model_name="vente",
            name="duration_days_connection",
            field=models.PositiveIntegerField(
                default=0,
                verbose_name="duration of the connection (in days, will be added to duration in months)",
            ),
        ),
        migrations.AlterField(
            model_name="vente",
            name="duration_days_membership",
            field=models.PositiveIntegerField(
                default=0,
                verbose_name="duration of the membership (in days, will be added to duration in months)",
            ),
        ),
    ]
