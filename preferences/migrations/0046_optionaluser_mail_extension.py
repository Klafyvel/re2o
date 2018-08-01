# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-06-26 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0045_remove_unused_payment_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionaluser',
            name='local_email_accounts_enabled',
            field=models.BooleanField(default=False, help_text='Enable local email accounts for users'),
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='local_email_domain',
            field=models.CharField(default='@example.org', help_text='Domain to use for local email accounts', max_length=32),
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='max_email_address',
            field=models.IntegerField(default=15, help_text='Maximum number of local email address for a standard user'),
        ),
    ]
