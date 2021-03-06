# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-19 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0069_optionaluser_disable_emailnotyetconfirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optionaluser',
            name='self_change_room',
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='self_room_policy',
            field=models.CharField(choices=[('DISABLED', "Users can't select their room"), ('ONLY_INACTIVE', 'Users can only select a room occupied by a user with a disabled connection.'), ('ALL_ROOM', 'Users can select all rooms')], default='DISABLED', help_text='Policy on self users room edition', max_length=32),
        ),
    ]
