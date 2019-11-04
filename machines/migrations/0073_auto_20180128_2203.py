# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-28 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("machines", "0072_auto_20180108_1822")]

    operations = [
        migrations.CreateModel(
            name="Ipv6List",
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
                ("ipv6", models.GenericIPAddressField(protocol="IPv6", unique=True)),
                ("slaac_ip", models.BooleanField(default=False)),
                (
                    "interface",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="machines.Interface",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="ipv6list", unique_together=set([("interface", "slaac_ip")])
        ),
    ]
