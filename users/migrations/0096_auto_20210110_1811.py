# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-01-10 17:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0095_user_theme'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LdapServiceUser',
        ),
        migrations.DeleteModel(
            name='LdapServiceUserGroup',
        ),
        migrations.DeleteModel(
            name='LdapUser',
        ),
        migrations.DeleteModel(
            name='LdapUserGroup',
        ),
    ]
