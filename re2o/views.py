# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
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
"""
Fonctions de la page d'accueil et diverses fonctions utiles pour tous
les views
"""

from __future__ import unicode_literals

from django.shortcuts import render
from django.template.context_processors import csrf
from preferences.models import Service


def form(ctx, template, request):
    """Form générique, raccourci importé par les fonctions views du site"""
    context = ctx
    context.update(csrf(request))
    return render(request, template, context)


def index(request):
    """Affiche la liste des services sur la page d'accueil de re2o"""
    services = [[], [], []]
    for indice, serv in enumerate(Service.objects.all()):
        services[indice % 3].append(serv)
    return form({'services_urls': services}, 're2o/index.html', request)
