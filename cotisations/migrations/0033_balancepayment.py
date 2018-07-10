# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-07-03 13:53
from __future__ import unicode_literals

import cotisations.payment_methods.mixins
from django.db import migrations, models
import django.db.models.deletion


def add_solde(apps, schema_editor):
    OptionalUser = apps.get_model('preferences', 'OptionalUser')
    options, _created = OptionalUser.objects.get_or_create()

    Payment = apps.get_model('cotisations', 'Paiement')
    BalancePayment = apps.get_model('cotisations', 'BalancePayment')

    solde, _created = Payment.objects.get_or_create(moyen="solde")
    balance = BalancePayment()
    balance.payment = solde
    balance.minimum_balance = options.solde_negatif
    balance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cotisations', '0032_chequepayment_comnpaypayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalancePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_balance', models.DecimalField(decimal_places=2, help_text='The minimal amount of money allowed for the balance at the end of a payment. You can specify negative amount.', max_digits=5, verbose_name='Minimum balance')),
                ('payment', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to='cotisations.Paiement')),
            ],
            bases=(cotisations.payment_methods.mixins.PaymentMethodMixin, models.Model),
        ),
        migrations.RunPython(add_solde)
    ]
