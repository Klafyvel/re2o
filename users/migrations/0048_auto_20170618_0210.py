# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-18 00:10
from __future__ import unicode_literals

from django.db import migrations
import ldapdb.models.fields


class Migration(migrations.Migration):

    dependencies = [("users", "0047_auto_20170618_0156")]

    operations = [
        migrations.AlterField(
            model_name="ldapserviceusergroup",
            name="name",
            field=ldapdb.models.fields.CharField(
                db_column="cn", max_length=200, primary_key=True, serialize=False
            ),
        )
    ]
