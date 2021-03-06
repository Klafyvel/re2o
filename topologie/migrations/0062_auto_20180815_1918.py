# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-08-15 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("topologie", "0061_portprofile")]

    operations = [
        migrations.AlterModelOptions(
            name="accesspoint",
            options={
                "permissions": (
                    ("view_accesspoint", "Can view an access point object"),
                ),
                "verbose_name": "access point",
                "verbose_name_plural": "access points",
            },
        ),
        migrations.AlterModelOptions(
            name="building",
            options={
                "permissions": (("view_building", "Can view a building object"),),
                "verbose_name": "building",
                "verbose_name_plural": "buildings",
            },
        ),
        migrations.AlterModelOptions(
            name="constructorswitch",
            options={
                "permissions": (
                    ("view_constructorswitch", "Can view a switch constructor object"),
                ),
                "verbose_name": "switch constructor",
                "verbose_name_plural": "switch constructors",
            },
        ),
        migrations.AlterModelOptions(
            name="modelswitch",
            options={
                "permissions": (
                    ("view_modelswitch", "Can view a switch model object"),
                ),
                "verbose_name": "switch model",
                "verbose_name_plural": "switch models",
            },
        ),
        migrations.AlterModelOptions(
            name="port",
            options={
                "permissions": (("view_port", "Can view a port object"),),
                "verbose_name": "port",
                "verbose_name_plural": "ports",
            },
        ),
        migrations.AlterModelOptions(
            name="portprofile",
            options={
                "permissions": (
                    ("view_port_profile", "Can view a port profile object"),
                ),
                "verbose_name": "port profile",
                "verbose_name_plural": "port profiles",
            },
        ),
        migrations.AlterModelOptions(
            name="room",
            options={
                "ordering": ["name"],
                "permissions": (("view_room", "Can view a room object"),),
                "verbose_name": "room",
                "verbose_name_plural": "rooms",
            },
        ),
        migrations.AlterModelOptions(
            name="stack",
            options={
                "permissions": (("view_stack", "Can view a stack object"),),
                "verbose_name": "switches stack",
                "verbose_name_plural": "switches stacks",
            },
        ),
        migrations.AlterModelOptions(
            name="switch",
            options={
                "permissions": (("view_switch", "Can view a switch object"),),
                "verbose_name": "switch",
                "verbose_name_plural": "switches",
            },
        ),
        migrations.AlterModelOptions(
            name="switchbay",
            options={
                "permissions": (("view_switchbay", "Can view a switch bay object"),),
                "verbose_name": "switch bay",
                "verbose_name_plural": "switch bays",
            },
        ),
        migrations.AlterField(
            model_name="accesspoint",
            name="location",
            field=models.CharField(
                blank=True,
                help_text="Details about the AP's location",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="port",
            name="state",
            field=models.BooleanField(
                default=True,
                help_text="Port state Active",
                verbose_name="Port state Active",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="arp_protect",
            field=models.BooleanField(
                default=False,
                help_text="Check if IP adress is DHCP assigned",
                verbose_name="ARP protection",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="dhcp_snooping",
            field=models.BooleanField(
                default=False,
                help_text="Protect against rogue DHCP",
                verbose_name="DHCP snooping",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="dhcpv6_snooping",
            field=models.BooleanField(
                default=False,
                help_text="Protect against rogue DHCPv6",
                verbose_name="DHCPv6 snooping",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="flow_control",
            field=models.BooleanField(default=False, help_text="Flow control"),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="loop_protect",
            field=models.BooleanField(
                default=False,
                help_text="Protect against loop",
                verbose_name="Loop protection",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="mac_limit",
            field=models.IntegerField(
                blank=True,
                help_text="Limit of MAC-address on this port",
                null=True,
                verbose_name="MAC limit",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="profil_default",
            field=models.CharField(
                blank=True,
                choices=[
                    ("room", "room"),
                    ("accespoint", "accesspoint"),
                    ("uplink", "uplink"),
                    ("asso_machine", "asso_machine"),
                    ("nothing", "nothing"),
                ],
                max_length=32,
                null=True,
                unique=True,
                verbose_name="Default profile",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="ra_guard",
            field=models.BooleanField(
                default=False,
                help_text="Protect against rogue RA",
                verbose_name="RA guard",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="radius_mode",
            field=models.CharField(
                choices=[("STRICT", "STRICT"), ("COMMON", "COMMON")],
                default="COMMON",
                help_text="In case of MAC-authentication : mode COMMON or STRICT on this port",
                max_length=32,
                verbose_name="RADIUS mode",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="radius_type",
            field=models.CharField(
                choices=[
                    ("NO", "NO"),
                    ("802.1X", "802.1X"),
                    ("MAC-radius", "MAC-radius"),
                ],
                help_text="Type of RADIUS authentication : inactive, MAC-address or 802.1X",
                max_length=32,
                verbose_name="RADIUS type",
            ),
        ),
        migrations.AlterField(
            model_name="portprofile",
            name="speed",
            field=models.CharField(
                choices=[
                    ("10-half", "10-half"),
                    ("100-half", "100-half"),
                    ("10-full", "10-full"),
                    ("100-full", "100-full"),
                    ("1000-full", "1000-full"),
                    ("auto", "auto"),
                    ("auto-10", "auto-10"),
                    ("auto-100", "auto-100"),
                ],
                default="auto",
                help_text="Port speed limit",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="switch",
            name="model",
            field=models.ForeignKey(
                blank=True,
                help_text="Switch model",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="topologie.ModelSwitch",
            ),
        ),
        migrations.AlterField(
            model_name="switch",
            name="number",
            field=models.PositiveIntegerField(help_text="Number of ports"),
        ),
        migrations.AlterField(
            model_name="switch",
            name="stack_member_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="switch",
            name="switchbay",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="topologie.SwitchBay",
            ),
        ),
        migrations.AlterField(
            model_name="switchbay",
            name="info",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
