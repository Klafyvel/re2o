# Re2o est un logiciel d'administration développé initiallement au Rézo Metz. Il
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
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0014_auto_20160704_1548")]

    operations = [
        migrations.CreateModel(
            name="Whitelist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("raison", models.CharField(max_length=255)),
                ("date_start", models.DateTimeField(auto_now_add=True)),
                ("date_end", models.DateTimeField(help_text="%m/%d/%y %H:%M:%S")),
                (
                    "user",
                    models.ForeignKey(
                        to="users.User", on_delete=django.db.models.deletion.PROTECT
                    ),
                ),
            ],
        )
    ]
