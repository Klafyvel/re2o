# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-15 10:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0077_auto_20180409_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='srv',
            name='priority',
            field=models.PositiveIntegerField(default=0, help_text="La priorité du serveur cible (valeur entière non négative, plus elle est faible, plus ce serveur sera utilisé s'il est disponible)", validators=[django.core.validators.MaxValueValidator(65535)]),
        ),
    ]
