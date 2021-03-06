# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-21 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0089_auto_20200418_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='External email address allowing us to contact you.', max_length=254),
        ),
    ]
