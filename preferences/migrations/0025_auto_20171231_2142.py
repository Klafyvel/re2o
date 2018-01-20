# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-31 20:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0024_optionaluser_all_can_create'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assooption',
            options={'permissions': (('view_assooption', "Peut voir les options de l'asso"),)},
        ),
        migrations.AlterModelOptions(
            name='generaloption',
            options={'permissions': (('view_generaloption', 'Peut voir les options générales'),)},
        ),
        migrations.AlterModelOptions(
            name='mailmessageoption',
            options={'permissions': (('view_mailmessageoption', 'Peut voir les options de mail'),)},
        ),
        migrations.AlterModelOptions(
            name='optionalmachine',
            options={'permissions': (('view_optionalmachine', 'Peut voir les options de machine'),)},
        ),
        migrations.AlterModelOptions(
            name='optionaltopologie',
            options={'permissions': (('view_optionaltopologie', 'Peut voir les options de topologie'),)},
        ),
        migrations.AlterModelOptions(
            name='optionaluser',
            options={'permissions': (('view_optionaluser', "Peut voir les options de l'user"),)},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'permissions': (('view_service', 'Peut voir les options de service'),)},
        ),
    ]