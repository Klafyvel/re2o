# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-18 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0092_auto_20200502_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
