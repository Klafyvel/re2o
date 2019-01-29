# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2019 Arthur Grisel-Davy
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

"""Defines the serializers of the API
"""

from rest_framework import serializers

import cotisations.models as cotisations

from re2o.serializers import NamespacedHRField, NamespacedHIField, NamespacedHMSerializer

class FactureSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Facture` objects.
    """

    class Meta:
        model = cotisations.Facture
        fields = ('user', 'paiement', 'banque', 'cheque', 'date', 'valid',
                  'control', 'prix_total', 'name', 'api_url')


class BaseInvoiceSerializer(NamespacedHMSerializer):
    class Meta:
        model = cotisations.BaseInvoice
        fields = ('__all__')

class VenteSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Vente` objects.
    """

    class Meta:
        model = cotisations.Vente
        fields = ('facture',
                  'number', 'name', 'prix', 'duration',
                  'type_cotisation', 'prix_total', 'api_url')


class ArticleSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Article` objects.
    """

    class Meta:
        model = cotisations.Article
        fields = ('name', 'prix', 'duration', 'type_user',
                  'type_cotisation', 'api_url')


class BanqueSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Banque` objects.
    """

    class Meta:
        model = cotisations.Banque
        fields = ('name', 'api_url')


class PaiementSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Paiement` objects.
    """

    class Meta:
        model = cotisations.Paiement
        fields = ('moyen', 'api_url')


class CotisationSerializer(NamespacedHMSerializer):
    """Serialize `cotisations.models.Cotisation` objects.
    """

    class Meta:
        model = cotisations.Cotisation
        fields = ('vente', 'type_cotisation', 'date_start', 'date_end',
                  'api_url')
