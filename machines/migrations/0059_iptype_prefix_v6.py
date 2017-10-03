# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-02 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0058_auto_20171002_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='iptype',
            name='prefix_v6',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='IPv6'),
        ),
    ]
