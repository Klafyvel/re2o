# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au Rézo Metz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2021  Yohann D'ANELLO
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
This app provides a clean way to make a subscription,
to make a captive portal.

This is only sugar, this does not provide any model.
"""

from cotisations.views import new_facture
from django.conf.urls import url
from django.contrib.auth.views import LoginView

from .views import IndexView, SignUpView

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^signup/$", SignUpView.as_view(), name="signup"),
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^extend-connection/(?P<userid>[0-9]+)/$", new_facture, name="extend-connection"),
]