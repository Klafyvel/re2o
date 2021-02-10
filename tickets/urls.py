# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au Rézo Metz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2019  Arthur Grisel-Davy
# Copyright © 2020  Gabriel Détraz
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
Tickets url
"""

from django.urls import path, re_path

from . import views
from .preferences.views import edit_options

app_name = "tickets"

urlpatterns = [
    path("", views.aff_tickets, name="aff-tickets"),
    path("<int:ticketid>", views.aff_ticket, name="aff-ticket"),
    path(
        "change_ticket_status/<int:ticketid>",
        views.change_ticket_status,
        name="change-ticket-status",
    ),
    path("edit_ticket/<int:ticketid>", views.edit_ticket, name="edit-ticket"),
    re_path(
        r"^edit_options/(?P<section>TicketOption)$",
        edit_options,
        name="edit-options",
    ),
    path("new_ticket", views.new_ticket, name="new-ticket"),
    path("add_comment/<int:ticketid>", views.add_comment, name="add-comment"),
    path("edit_comment/<int:commentticketid>", views.edit_comment, name="edit-comment"),
    path("del_comment/<int:commentticketid>", views.del_comment, name="del-comment"),
]
