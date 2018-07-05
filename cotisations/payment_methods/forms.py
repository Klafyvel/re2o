from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l

from . import PAYMENT_METHODS
from cotisations.utils import find_payment_method

def payment_method_factory(payment, *args, creation=True, **kwargs):
    payment_method = kwargs.pop('instance', find_payment_method(payment))
    if payment_method is not None:
        return forms.modelform_factory(type(payment_method), fields='__all__')(
            *args,
            instance=payment_method,
            **kwargs
        )
    elif creation:
        return PaymentMethodForm(payment_method, *args, **kwargs)
    else:
        return forms.Form()


class PaymentMethodForm(forms.Form):
    """A special form which allows you to add a payment method to a `Payment`
    objects if it hasn't one yet, or to edit the existing payment method.

    To do so it replaces itself with a `modelform_factory`.
    """

    payment_method = forms.ChoiceField(
        label=_l("Special payment method"),
        help_text=_l("Warning : You will not be able to change the payment "
                     "method later. But you will be allowed to edit its "
                     "options."
        ),
        required=False
    )

    def __init__(self, payment_method, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)
        if payment_method is None:
            prefix = kwargs.get('prefix', None)
            self.fields['payment_method'].choices = [(i,p.NAME) for (i,p) in enumerate(PAYMENT_METHODS)]
            self.fields['payment_method'].choices.insert(0, ('', _l('no')))
            self.fields['payment_method'].widget.attrs = {
                'id': 'paymentMethodSelect'
            }
            self.templates = [
                forms.modelform_factory(p.PaymentMethod, fields='__all__')(prefix=prefix)
                for p in PAYMENT_METHODS
            ]
        else:
            self.fields = {}

    def clean(self):
        super(PaymentMethodForm, self).clean()
        choice = self.cleaned_data['payment_method']
        if choice=='':
            return
        choice = int(choice)
        model = PAYMENT_METHODS[choice].PaymentMethod
        form = forms.modelform_factory(model, fields='__all__')(self.data, prefix=self.prefix)
        self.payment_method = form.save(commit=False)
        if hasattr(self.payment_method, 'valid_form'):
            self.payment_method.valid_form(self)
        return self.cleaned_data



    def save(self, payment, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        self.payment_method.payment = payment
        if hasattr(self.payment_method, 'alter_payment'):
            self.payment_method.alter_payment(payment)
        if commit:
            payment.save()
            self.payment_method.save()
        return self.payment_method
