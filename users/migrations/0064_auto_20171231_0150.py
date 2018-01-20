# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-31 00:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0063_auto_20171231_0140'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='right',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='right',
            name='right',
        ),
        migrations.RemoveField(
            model_name='right',
            name='user',
        ),
        migrations.DeleteModel(
            name='Right',
        ),
        migrations.RemoveField(
            model_name='listright',
            name='id',
        ),
        migrations.AlterField(
            model_name='listright',
            name='group_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group'),
        ),

    ]