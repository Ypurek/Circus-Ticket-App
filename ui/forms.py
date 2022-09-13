from django import forms
from django.core.validators import validate_email
from core.validators import *
from django.core.exceptions import ValidationError


def check_if_interval(value):
    try:
        pair = value.split(',')
        int(pair[0])
        int(pair[1])
    except Exception:
        raise ValidationError('interval provided in wrong format', params={'value': value})


class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=1,
                               # BUG 9
                               max_length=9,
                               validators=[validate_chars, validate_user_not_exists])
    password = forms.CharField(label='password',
                               min_length=1,
                               max_length=8,
                               validators=[validate_chars])


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=1,
                               # BUG 9
                               max_length=9,
                               validators=[validate_chars, validate_user_exists])
    password = forms.CharField(label='password',
                               min_length=1,
                               max_length=8,
                               validators=[validate_chars])


class EditableUserInfo(forms.Form):
    email = forms.CharField(label='email',
                            max_length=50,
                            required=False,
                            validators=[validate_email])
    creditCard = forms.CharField(label='creditCard',
                                 required=False,
                                 max_length=19,
                                 validators=[is_credit_card, validate_credit_card_exists])
    deliveryAddress = forms.CharField(label='address',
                                      max_length=300,
                                      required=False)


class SimpleTicketSearchForm(forms.Form):
    date_from = forms.DateField(required=False,
                                label='Date From',
                                input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'],
                                widget=forms.TextInput(attrs={'class': 'formInput dateInput'}))
    date_to = forms.DateField(required=False,
                              label='Date To',
                              input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'],
                              widget=forms.TextInput(attrs={'class': 'formInput dateInput'}))
    time_interval = forms.CharField(required=False,
                                        label='Time',
                                        widget=forms.TextInput(attrs={'class': 'timeSlider'}),
                                    validators=[check_if_interval])
    price_interval = forms.CharField(required=False,
                                         label='Price',
                                         widget=forms.TextInput(attrs={'class': 'priceSlider'}),
                                     validators=[check_if_interval])
    keyword = forms.CharField(required=False,
                              label='Keyword',
                              widget=forms.TextInput(attrs={'class': 'formInput keyInput'}))



