# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-07-05 13:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("preferences", "0044_remove_payment_pass"),
        ("cotisations", "0030_custom_payment"),
    ]

    operations = [
        migrations.RemoveField(model_name="assooption", name="payment"),
        migrations.RemoveField(model_name="assooption", name="payment_id"),
        migrations.RemoveField(
            model_name="optionaluser", name="allow_self_subscription"
        ),
        migrations.RemoveField(model_name="optionaluser", name="max_solde"),
        migrations.RemoveField(model_name="optionaluser", name="min_online_payment"),
        migrations.RemoveField(model_name="optionaluser", name="solde_negatif"),
        migrations.RemoveField(model_name="optionaluser", name="user_solde"),
    ]
