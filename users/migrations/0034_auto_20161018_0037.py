# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Lara Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ldapdb.models.fields
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_remove_ldapuser_loginshell'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='ldapuser',
                    name='login_shell',
                    field=ldapdb.models.fields.CharField(blank=True, db_column='loginShell', max_length=200, null=True),
                ),
            ],
            database_operations=[
                migrations.RunSQL('ALTER TABLE users_ldapuser ADD COLUMN "loginShell" varchar(200) NULL;')
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='rezo_rez_uid',
            field=models.IntegerField(blank=True, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uid_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='users.School', null=True),
        ),
    ]
