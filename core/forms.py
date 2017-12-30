from django import forms
from .validators import *


class GetPerformanceForm(forms.Form):
    date_from = forms.DateField(required=False,
                                label="Date From",
                                input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    date_to = forms.DateField(required=False,
                              label="Date To",
                              input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField(required=False)
    price_from = forms.FloatField(required=False)
    price_to = forms.FloatField(required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)


class CreditCardForm(forms.Form):
    card_number = forms.CharField(required=False,
                                  validators=[is_credit_card, is_credit_card_unique])
    amount = forms.FloatField(required=False,
                              min_value=0)


class DiscountForm(forms.Form):
    code = forms.CharField(required=False,
                           max_length=50)
    percent = forms.IntegerField(required=False,
                                 max_value=20,
                                 min_value=1)