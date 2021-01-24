# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-20 17:19
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cotisations', '0043_separation_membership_connection_p1'),
    ]

    def split_dates(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        cotisation = apps.get_model("cotisations", "Cotisation")
        cotisations = cotisation.objects.using(db_alias).all()
        for cotis in cotisations:
            cotis.date_start_con = cotis.date_start
            cotis.date_start_memb = cotis.date_start
            cotis.date_end_con = cotis.date_end
            cotis.date_end_memb = cotis.date_end
            if cotis.type_cotisation == 'Connexion':
                cotis.date_end_memb = cotis.date_start
            if cotis.type_cotisation == 'Adhesion':
                cotis.date_end_con = cotis.date_start
            cotis.save()



    def split_duration_articles_and_ventes(apps, schema_editor):
        def split_duration(e):
            e.duration_membership = e.duration
            e.duration_connection = e.duration
            e.duration_days_membership = e.duration_days
            e.duration_days_connection = e.duration_days
            if e.type_cotisation == 'Connexion':
                e.duration_membership = 0
                e.duration_days_membership = 0
            if e.type_cotisation == 'Adhesion':
                e.duration_connection = 0
                e.duration_days_connection = 0
            e.save()
        db_alias = schema_editor.connection.alias
        article = apps.get_model("cotisations", "Article")
        vente = apps.get_model("cotisations", "Vente")
        for a in article.objects.using(db_alias).all():
            split_duration(a)
        for v in vente.objects.using(db_alias).all():
            split_duration(v)

    def unsplit_dates(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        cotisation = apps.get_model("cotisations", "Cotisation")
        cotisations = cotisation.objects.using(db_alias).all()
        for cotis in cotisations:
            connection = cotis.date_start_con != cotis.date_end_con
            adhesion = cotis.date_start_memb != cotis.date_end_memb
            cotis.date_start = cotis.date_start_con
            cotis.date_end = max(cotis.date_end_con, cotis.date_end_memb)
            if connection:
                cotis.type_cotisation = 'Connexion'
            if adhesion:
                cotis.type_cotisation = 'Adhesion'
            if connection and adhesion:
                cotis.type_cotisation = 'All'
            if not (connection or adhesion):
                cotis.type_cotisation = None
            cotis.save()



    def unsplit_duration_articles_and_ventes(apps, schema_editor):
        def unsplit_duration(e):
            e.duration = max(e.duration_membership, e.duration_connection)
            e.duration_days = max(e.duration_days_membership, e.duration_days_connection)
            connection = not (((e.duration_connection == 0) or (e.duration_connection__isnull)) and \
                              ((e.duration_days_connection == 0) or (e.duration_days_connection__isnull)))
            membership = not (((e.duration_membership == 0) or (e.duration_membership__isnull)) and \
                              ((e.duration_days_membership == 0) or (e.duration_days_membership__isnull)))
            if connection:
                e.type_cotisation = 'Connection'
            if membership:
                e.type_cotisation = 'Adhesion'
            if connection and membership:
                e.type_cotisation = 'All'
            if not (connection or membership):
                e.type_cotisation = None
            e.save()
        db_alias = schema_editor.connection.alias
        article = apps.get_model("cotisations", "Article")
        vente = apps.get_model("cotisations", "Vente")
        for a in article.objects.using(db_alias).all():
            unsplit_duration(a)
        for v in vente.objects.using(db_alias).all():
            unsplit_duration(v)


    operations = [
        migrations.RunPython(split_dates, unsplit_dates),
        migrations.RunPython(split_duration_articles_and_ventes, unsplit_duration_articles_and_ventes),
#        migrations.RemoveField(
#            model_name='article',
#            name='duration',
#        ),
#        migrations.RemoveField(
#            model_name='article',
#            name='duration_days',
#        ),
#        migrations.RemoveField(
#            model_name='article',
#            name='type_cotisation',
#        ),
#        migrations.RemoveField(
#            model_name='cotisation',
#            name='date_end',
#        ),
#        migrations.RemoveField(
#            model_name='cotisation',
#            name='date_start',
#        ),
#        migrations.RemoveField(
#            model_name='cotisation',
#            name='type_cotisation',
#        ),
#        migrations.RemoveField(
#            model_name='vente',
#            name='duration',
#        ),
#        migrations.RemoveField(
#            model_name='vente',
#            name='duration_days',
#        ),
#        migrations.RemoveField(
#            model_name='vente',
#            name='type_cotisation',
#        ),
    ]
