# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-08 02:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topologie', '0057_auto_20180408_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='location',
        ),
    ]
