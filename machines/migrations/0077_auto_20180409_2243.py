# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-09 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0076_auto_20180130_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extension',
            name='origin',
            field=models.ForeignKey(blank=True, help_text='Enregistrement A associé à la zone', null=True, on_delete=django.db.models.deletion.PROTECT, to='machines.IpList'),
        ),
    ]
