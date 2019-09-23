# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-21 18:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
import re2o.mixins


def create_current_mandate(apps, schema_editor):
    AssoOption = apps.get_model('preferences', 'AssoOption')
    Mandate = apps.get_model('preferences', 'Mandate')
    Adherent = apps.get_model('users', 'Adherent')
    assooption = AssoOption.objects.get_or_create()[0]
    pres_name = assooption.pres_name
    l = pres_name.split(' ')
    try:
        name, surname = l[0], l[1]
        president = Adherent.objects.get(name__icontains=name, surname__icontains=surname)
        Mandate.objects.create(
            president=president,
            start_date=timezone.now(),
        )
    except Exception as e:
        print("Warning : I was unable to find an adherent corresponding to %s. You might want to edit your preferences afterward. I will disable the sending of vouchers by email." % pres_name)
        CotisationsOption = apps.get_model('preferences', 'CotisationsOption')
        cotisoption = CotisationsOption.objects.get_or_create()[0]
        cotisoption.send_voucher_mail = False
        cotisoption.save()



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('preferences', '0062_auto_20190910_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='end date')),
                ('president', models.ForeignKey(blank=True, help_text='Displayed on subscription vouchers', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='President of the association')),
            ],
            options={
                'verbose_name': 'Mandate',
                'verbose_name_plural': 'Mandates',
                'permissions': (('view_mandate', 'Can view a mandate'),),
            },
            bases=(re2o.mixins.RevMixin, re2o.mixins.AclMixin, models.Model),
        ),
        migrations.RunPython(create_current_mandate),
        migrations.AlterField(
            model_name='cotisationsoption',
            name='send_voucher_mail',
            field=models.BooleanField(default=False, help_text='Be carefull, if no mandate is defined on the preferences page, errors will be triggered when generating vouchers.', verbose_name='Send voucher by email when the invoice is controlled.'),
        ),
        migrations.RemoveField(
            model_name='assooption',
            name='pres_name',
        ),
    ]
