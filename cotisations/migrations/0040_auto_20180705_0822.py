# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-07-05 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisations', '0039_auto_20180704_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancepayment',
            name='minimum_balance',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The minimal amount of money allowed for the balance at the end of a payment. You can specify negative amount.', max_digits=5, verbose_name='Minimum balance'),
        ),
    ]
