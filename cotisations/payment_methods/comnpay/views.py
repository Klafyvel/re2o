# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2018  Hugo Levy-Falk
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
"""Payment

Here are the views needed by comnpay
"""

from collections import OrderedDict

from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseBadRequest

from cotisations.models import Facture
from .comnpay import Transaction
from .models import ComnpayPayment

from cotisations.utils import send_mail_invoice

@csrf_exempt
@login_required
def accept_payment(request, factureid):
    """
    The view where the user is redirected when a comnpay payment has been
    accepted.
    """
    invoice = get_object_or_404(Facture, id=factureid)
    if invoice.valid:
        messages.success(
            request,
            _("The payment of %(amount)s € was accepted.") % {
                'amount': invoice.prix_total()
            }
        )
        # In case a cotisation was bought, inform the user, the
        # cotisation time has been extended too
        if any(purchase.type_cotisation
               for purchase in invoice.vente_set.all()):
            messages.success(
                request,
                _("The subscription of %(member_name)s was extended to"
                  " %(end_date)s.") % {
                    'member_name': request.user.pseudo,
                    'end_date': request.user.end_adhesion()
                }
            )
    return redirect(reverse(
        'users:profil',
        kwargs={'userid': request.user.id}
    ))


@csrf_exempt
@login_required
def refuse_payment(request):
    """
    The view where the user is redirected when a comnpay payment has been
    refused.
    """
    messages.error(
        request,
        _("The payment was refused.")
    )
    return redirect(reverse(
        'users:profil',
        kwargs={'userid': request.user.id}
    ))


@csrf_exempt
def ipn(request):
    """
    The view called by Comnpay server to validate the transaction.
    Verify that we can firmly save the user's action and notify
    Comnpay with 400 response if not or with a 200 response if yes.
    """
    p = Transaction()
    order = ('idTpe', 'idTransaction', 'montant', 'result', 'sec', )
    try:
        data = OrderedDict([(f, request.POST[f]) for f in order])
    except MultiValueDictKeyError:
        return HttpResponseBadRequest("HTTP/1.1 400 Bad Request")

    idTransaction = request.POST['idTransaction']
    try:
        factureid = int(idTransaction)
    except ValueError:
        return HttpResponseBadRequest("HTTP/1.1 400 Bad Request")

    facture = get_object_or_404(Facture, id=factureid)
    payment_method = get_object_or_404(
        ComnpayPayment, payment=facture.paiement)

    if not p.validSec(data, payment_method.payment_pass):
        return HttpResponseBadRequest("HTTP/1.1 400 Bad Request")

    result = True if (request.POST['result'] == 'OK') else False
    idTpe = request.POST['idTpe']

    # Checking that the payment is actually for us.
    if not idTpe == payment_method.payment_credential:
        return HttpResponseBadRequest("HTTP/1.1 400 Bad Request")

        # Checking that the payment is valid
    if not result:
        # Payment failed: Cancelling the invoice operation
        # And send the response to Comnpay indicating we have well
        # received the failure information.
        return HttpResponse("HTTP/1.1 200 OK")

    facture.valid = True
    facture.save()

    send_mail_invoice(facture)

    # Everything worked we send a reponse to Comnpay indicating that
    # it's ok for them to proceed
    return HttpResponse("HTTP/1.0 200 OK")

