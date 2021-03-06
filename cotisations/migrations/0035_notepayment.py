# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-01 11:27
from __future__ import unicode_literals

import cotisations.payment_methods.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("cotisations", "0034_auto_20180831_1532")]

    operations = [
        migrations.CreateModel(
            name="NotePayment",
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
                ("server", models.CharField(max_length=255, verbose_name="server")),
                ("port", models.PositiveIntegerField(blank=True, null=True)),
                ("id_note", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "payment",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_method",
                        to="cotisations.Paiement",
                    ),
                ),
            ],
            options={"verbose_name": "NoteKfet"},
            bases=(cotisations.payment_methods.mixins.PaymentMethodMixin, models.Model),
        )
    ]
