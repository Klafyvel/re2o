# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-20 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topologie', '0072_auto_20190720_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='location',
            field=models.CharField(blank=True, help_text="Details about the AP's location.", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='moduleonswitch',
            name='slot',
            field=models.CharField(help_text='Slot on switch.', max_length=15, verbose_name='slot'),
        ),
        migrations.AlterField(
            model_name='moduleswitch',
            name='comment',
            field=models.CharField(blank=True, help_text='Comment.', max_length=255, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='moduleswitch',
            name='reference',
            field=models.CharField(help_text='Reference of a module.', max_length=255, verbose_name='module reference'),
        ),
        migrations.AlterField(
            model_name='port',
            name='state',
            field=models.BooleanField(default=True, help_text='Port state Active.', verbose_name='port state Active'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='arp_protect',
            field=models.BooleanField(default=False, help_text='Check if IP address is DHCP assigned.', verbose_name='ARP protection'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='dhcp_snooping',
            field=models.BooleanField(default=False, help_text='Protect against rogue DHCP.', verbose_name='DHCP snooping'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='dhcpv6_snooping',
            field=models.BooleanField(default=False, help_text='Protect against rogue DHCPv6.', verbose_name='DHCPv6 snooping'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='flow_control',
            field=models.BooleanField(default=False, help_text='Flow control.'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='loop_protect',
            field=models.BooleanField(default=False, help_text='Protect against loop.', verbose_name='loop protection'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='mac_limit',
            field=models.IntegerField(blank=True, help_text='Limit of MAC-address on this port.', null=True, verbose_name='MAC limit'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='on_dormitory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dormitory_ofprofil', to='topologie.Dormitory', verbose_name='profile on dormitory'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='profil_default',
            field=models.CharField(blank=True, choices=[('room', 'Room'), ('access_point', 'Access point'), ('uplink', 'Uplink'), ('asso_machine', 'Organisation machine'), ('nothing', 'Nothing')], max_length=32, null=True, verbose_name='default profile'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='ra_guard',
            field=models.BooleanField(default=False, help_text='Protect against rogue RA.', verbose_name='RA guard'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='radius_mode',
            field=models.CharField(choices=[('STRICT', 'STRICT'), ('COMMON', 'COMMON')], default='COMMON', help_text='In case of MAC-authentication: mode COMMON or STRICT on this port.', max_length=32, verbose_name='RADIUS mode'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='radius_type',
            field=models.CharField(choices=[('NO', 'NO'), ('802.1X', '802.1X'), ('MAC-radius', 'MAC-RADIUS')], help_text='Type of RADIUS authentication: inactive, MAC-address or 802.1X.', max_length=32, verbose_name='RADIUS type'),
        ),
        migrations.AlterField(
            model_name='portprofile',
            name='speed',
            field=models.CharField(choices=[('10-half', '10-half'), ('100-half', '100-half'), ('10-full', '10-full'), ('100-full', '100-full'), ('1000-full', '1000-full'), ('auto', 'auto'), ('auto-10', 'auto-10'), ('auto-100', 'auto-100')], default='auto', help_text='Port speed limit.', max_length=32),
        ),
        migrations.AlterField(
            model_name='switch',
            name='automatic_provision',
            field=models.BooleanField(default=False, help_text='Automatic provision for the switch.'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='management_creds',
            field=models.ForeignKey(blank=True, help_text='Management credentials for the switch.', null=True, on_delete=django.db.models.deletion.PROTECT, to='preferences.SwitchManagementCred'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='model',
            field=models.ForeignKey(blank=True, help_text='Switch model.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='topologie.ModelSwitch'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='number',
            field=models.PositiveIntegerField(help_text='Number of ports.'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='radius_key',
            field=models.ForeignKey(blank=True, help_text='RADIUS key of the switch.', null=True, on_delete=django.db.models.deletion.PROTECT, to='preferences.RadiusKey'),
        ),
    ]
