# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-07-02 18:56
from __future__ import unicode_literals

import re2o.aes_field
import cotisations.payment_methods.mixins
from django.db import migrations, models
import django.db.models.deletion


def add_cheque(apps, schema_editor):
    ChequePayment = apps.get_model("cotisations", "ChequePayment")
    Payment = apps.get_model("cotisations", "Paiement")
    for p in Payment.objects.filter(type_paiement=1):
        cheque = ChequePayment()
        cheque.payment = p
        cheque.save()


def add_comnpay(apps, schema_editor):
    ComnpayPayment = apps.get_model("cotisations", "ComnpayPayment")
    Payment = apps.get_model("cotisations", "Paiement")
    AssoOption = apps.get_model("preferences", "AssoOption")
    options, _created = AssoOption.objects.get_or_create()
    try:
        payment = Payment.objects.get(moyen="Rechargement en ligne")
    except Payment.DoesNotExist:
        return
    comnpay = ComnpayPayment()
    comnpay.payment_user = options.payment_id
    comnpay.payment = payment
    comnpay.save()
    payment.moyen = "ComnPay"

    payment.save()


def add_solde(apps, schema_editor):
    OptionalUser = apps.get_model("preferences", "OptionalUser")
    options, _created = OptionalUser.objects.get_or_create()

    Payment = apps.get_model("cotisations", "Paiement")
    BalancePayment = apps.get_model("cotisations", "BalancePayment")

    try:
        solde = Payment.objects.get(moyen="solde")
    except Payment.DoesNotExist:
        return
    balance = BalancePayment()
    balance.payment = solde
    balance.minimum_balance = options.solde_negatif
    balance.maximum_balance = options.max_solde
    solde.is_balance = True
    balance.save()
    solde.save()


class Migration(migrations.Migration):

    dependencies = [
        ("preferences", "0044_remove_payment_pass"),
        ("cotisations", "0029_auto_20180414_2056"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="paiement",
            options={
                "permissions": (
                    ("view_paiement", "Can see a payement's details"),
                    ("use_every_payment", "Can use every payement"),
                ),
                "verbose_name": "Payment method",
                "verbose_name_plural": "Payment methods",
            },
        ),
        migrations.AlterModelOptions(
            name="article",
            options={
                "permissions": (
                    ("view_article", "Can see an article's details"),
                    ("buy_every_article", "Can buy every_article"),
                ),
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
            },
        ),
        migrations.AddField(
            model_name="paiement",
            name="available_for_everyone",
            field=models.BooleanField(
                default=False, verbose_name="Is available for every user"
            ),
        ),
        migrations.AddField(
            model_name="paiement",
            name="is_balance",
            field=models.BooleanField(
                default=False,
                editable=False,
                help_text="There should be only one balance payment method.",
                verbose_name="Is user balance",
                validators=[cotisations.models.check_no_balance],
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="available_for_everyone",
            field=models.BooleanField(
                default=False, verbose_name="Is available for every user"
            ),
        ),
        migrations.CreateModel(
            name="ChequePayment",
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
            bases=(cotisations.payment_methods.mixins.PaymentMethodMixin, models.Model),
            options={"verbose_name": "Cheque"},
        ),
        migrations.CreateModel(
            name="ComnpayPayment",
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
                (
                    "payment_credential",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="ComNpay VAD Number",
                    ),
                ),
                (
                    "payment_pass",
                    re2o.aes_field.AESEncryptedField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="ComNpay Secret Key",
                    ),
                ),
                (
                    "payment",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_method",
                        to="cotisations.Paiement",
                    ),
                ),
                (
                    "minimum_payment",
                    models.DecimalField(
                        decimal_places=2,
                        default=1,
                        help_text="The minimal amount of money you have to use when paying with ComNpay",
                        max_digits=5,
                        verbose_name="Minimum payment",
                    ),
                ),
            ],
            bases=(cotisations.payment_methods.mixins.PaymentMethodMixin, models.Model),
            options={"verbose_name": "ComNpay"},
        ),
        migrations.CreateModel(
            name="BalancePayment",
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
                (
                    "minimum_balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="The minimal amount of money allowed for the balance at the end of a payment. You can specify negative amount.",
                        max_digits=5,
                        verbose_name="Minimum balance",
                    ),
                ),
                (
                    "payment",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_method",
                        to="cotisations.Paiement",
                    ),
                ),
                (
                    "maximum_balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=50,
                        help_text="The maximal amount of money allowed for the balance.",
                        max_digits=5,
                        verbose_name="Maximum balance",
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "credit_balance_allowed",
                    models.BooleanField(
                        default=False, verbose_name="Allow user to credit their balance"
                    ),
                ),
            ],
            bases=(cotisations.payment_methods.mixins.PaymentMethodMixin, models.Model),
            options={"verbose_name": "User Balance"},
        ),
        migrations.RunPython(add_comnpay),
        migrations.RunPython(add_cheque),
        migrations.RunPython(add_solde),
        migrations.RemoveField(model_name="paiement", name="type_paiement"),
    ]
