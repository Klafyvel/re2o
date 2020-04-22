# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
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

# App de gestion des users pour re2o
# Lara Kermarec, Gabriel Détraz, Lemesle Augustin
# Gplv2

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.forms import modelformset_factory
from re2o.views import form

from re2o.base import re2o_paginator

from re2o.acl import can_view, can_view_all, can_edit, can_create

from preferences.models import GeneralOption

from .models import Ticket

from .forms import NewTicketForm, EditTicketForm


def new_ticket(request):
    """ Ticket creation view"""
    ticketform = NewTicketForm(request.POST or None, request=request)
    if ticketform.is_valid():
        ticketform.save()
        messages.success(
            request,
            _(
                "Your ticket has been succesfully opened. We will take care of it as soon as possible."
            ),
        )
        if not request.user.is_authenticated:
            return redirect(reverse("index"))
        else:
            return redirect(
                 reverse("users:profil", kwargs={"userid": str(request.user.id)})
            )
    return form(
        {"ticketform": ticketform, 'action_name': ("Create a ticket")}, "tickets/edit.html", request
    )


@login_required
@can_view(Ticket)
def aff_ticket(request, ticket, ticketid):
    """View to display only one ticket"""
    return render(
        request,
        "tickets/aff_ticket.html",
        {"ticket": ticket},
    )


@login_required
@can_edit(Ticket)
def change_ticket_status(request, ticket, ticketid):
    """View to edit ticket state"""
    ticket.solved = not ticket.solved
    ticket.save()
    return redirect(
        reverse("tickets:aff-ticket", kwargs={"ticketid": str(ticketid)})
    )


@login_required
@can_edit(Ticket)
def edit_ticket(request, ticket, ticketid):
    """ Ticket creation view"""
    ticketform = EditTicketForm(request.POST or None, instance=ticket)
    if ticketform.is_valid():
        ticketform.save()
        messages.success(
            request,
            _(
                "Ticket has been updated successfully"
            ),
        )
        return redirect(
            reverse("tickets:aff-ticket", kwargs={"ticketid": str(ticketid)})
        )
    return form(
        {"ticketform": ticketform, 'action_name': ("Edit this ticket")}, "tickets/edit.html", request
    )


@login_required
@can_view_all(Ticket)
def aff_tickets(request):
    """ View to display all the tickets """
    tickets_list = Ticket.objects.all().order_by("-date")
    nbr_tickets = tickets_list.count()
    nbr_tickets_unsolved = tickets_list.filter(solved=False).count()
    if nbr_tickets:
        last_ticket_date = tickets_list.first().date
    else:
        last_ticket_date = _("Never")

    pagination_number = GeneralOption.get_cached_value("pagination_number")

    tickets = re2o_paginator(request, tickets_list, pagination_number)

    context = {
        "tickets_list": tickets,
        "last_ticket_date": last_ticket_date,
        "nbr_tickets": nbr_tickets,
        "nbr_tickets_unsolved": nbr_tickets_unsolved,
    }

    return render(request, "tickets/index.html", context=context)


# views cannoniques des apps optionnels
def profil(request, user):
    """ View to display the ticket's module on the profil"""
    tickets_list = Ticket.objects.filter(user=user).all().order_by("-date")
    nbr_tickets = tickets_list.count()
    nbr_tickets_unsolved = tickets_list.filter(solved=False).count()
    if nbr_tickets:
        last_ticket_date = tickets_list.first().date
    else:
        last_ticket_date = _("Never")

    pagination_number = GeneralOption.get_cached_value("pagination_large_number")

    tickets = re2o_paginator(request, tickets_list, pagination_number)

    context = {
        "tickets_list": tickets,
        "last_ticket_date": last_ticket_date,
        "nbr_tickets": nbr_tickets,
        "nbr_tickets_unsolved": nbr_tickets_unsolved,
    }
    return render_to_string(
        "tickets/profil.html", context=context, request=request, using=None
    )


def contact(request):
    """View to display a contact address on the contact page
    used here to display a link to open a ticket"""
    return render_to_string("tickets/contact.html")


def navbar_user():
    """View to display the ticket link in thet user's dropdown in the navbar"""
    return ("users", render_to_string("tickets/navbar.html"))


def navbar_logout():
    """View to display the ticket link to log out users"""
    return render_to_string("tickets/navbar_logout.html")
