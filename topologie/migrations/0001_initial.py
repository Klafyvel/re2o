# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('building', models.CharField(max_length=10)),
                ('number', models.IntegerField()),
                ('details', models.CharField(max_length=255, blank=True)),
            ],
        ),
    ]
