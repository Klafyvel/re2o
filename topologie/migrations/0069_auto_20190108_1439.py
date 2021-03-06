# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-01-08 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("topologie", "0068_auto_20190102_1758")]

    operations = [
        migrations.AlterModelOptions(
            name="moduleonswitch",
            options={
                "permissions": (
                    (
                        "view_moduleonswitch",
                        "Can view a link between switch and module object",
                    ),
                ),
                "verbose_name": "link between switch and module",
                "verbose_name_plural": "links between switch and module",
            },
        ),
        migrations.AlterModelOptions(
            name="moduleswitch",
            options={
                "permissions": (
                    ("view_moduleswitch", "Can view a switch module object"),
                ),
                "verbose_name": "switch module",
                "verbose_name_plural": "switch modules",
            },
        ),
        migrations.AlterField(
            model_name="modelswitch",
            name="is_itself_module",
            field=models.BooleanField(
                default=False, help_text="The switch is considered as a module."
            ),
        ),
        migrations.AlterField(
            model_name="modelswitch",
            name="is_modular",
            field=models.BooleanField(
                default=False, help_text="The switch model is modular."
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="profil_default",
            field=models.CharField(
                blank=True,
                choices=[
                    ("room", "Room"),
                    ("access_point", "Access point"),
                    ("uplink", "Uplink"),
                    ("asso_machine", "Organisation machine"),
                    ("nothing", "Nothing"),
                ],
                max_length=32,
                null=True,
                unique=True,
                verbose_name="Default profile",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="radius_type",
            field=models.CharField(
                choices=[
                    ("NO", "NO"),
                    ("802.1X", "802.1X"),
                    ("MAC-radius", "MAC-RADIUS"),
                ],
                help_text="Type of RADIUS authentication : inactive, MAC-address or 802.1X",
                max_length=32,
                verbose_name="RADIUS type",
            ),
        ),
        migrations.AlterField(
            model_name="switch",
            name="automatic_provision",
            field=models.BooleanField(
                default=False, help_text="Automatic provision for the switch"
            ),
        ),
        migrations.AlterField(
            model_name="switch",
            name="management_creds",
            field=models.ForeignKey(
                blank=True,
                help_text="Management credentials for the switch",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="preferences.SwitchManagementCred",
            ),
        ),
        migrations.AlterField(
            model_name="switch",
            name="radius_key",
            field=models.ForeignKey(
                blank=True,
                help_text="RADIUS key of the switch",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="preferences.RadiusKey",
            ),
        ),
    ]
