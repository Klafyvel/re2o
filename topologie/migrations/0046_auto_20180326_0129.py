# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-25 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("topologie", "0045_auto_20180326_0123")]

    operations = [
        migrations.AlterUniqueTogether(
            name="port", unique_together=set([("switch", "port")])
        )
    ]
