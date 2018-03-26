# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-31 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topologie', '0037_auto_20180325_0127'),
    ]

    def transfer_sw(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        newswitch = apps.get_model("topologie", "NewSwitch")
        switch = apps.get_model("topologie", "Switch")
        interface =  apps.get_model("machines", "Interface")
        sw_list = switch.objects.using(db_alias).all()
        for sw in sw_list:
            new_sw = newswitch()
            new_sw.location = sw.location
            new_sw.number = sw.number
            new_sw.details = sw.details
            new_sw.stack = sw.stack
            new_sw.stack_member_id = sw.stack_member_id
            new_sw.model = sw.model
            new_sw.interface_ptr_id = sw.switch_interface.pk
            new_sw.__dict__.update(sw.switch_interface.__dict__) 
            new_sw.save()

    def untransfer_sw(apps, schema_editor):
        return

    operations = [
    migrations.RunPython(transfer_sw, untransfer_sw),
    ]
