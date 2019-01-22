# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-01-08 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0079_auto_20181228_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Disabled'), (2, 'Archived'), (3, 'Not yet active')], default=3),
        ),
    ]
