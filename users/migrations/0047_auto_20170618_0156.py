# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-17 23:56
from __future__ import unicode_literals

from django.db import migrations, models
import ldapdb.models.fields


class Migration(migrations.Migration):

    dependencies = [("users", "0046_auto_20170617_1433")]

    operations = [
        migrations.CreateModel(
            name="LdapServiceUserGroup",
            fields=[
                (
                    "dn",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                (
                    "name",
                    ldapdb.models.fields.CharField(
                        db_column="cn", max_length=200, serialize=False
                    ),
                ),
                (
                    "members",
                    ldapdb.models.fields.ListField(blank=True, db_column="member"),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="serviceuser",
            name="access_group",
            field=models.IntegerField(
                choices=[(0, "auth"), (1, "readonly"), (2, "usermgmt")], default=1
            ),
        ),
    ]
