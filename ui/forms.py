from django import forms
from django.core.validators import validate_email
from core.validators import *


class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=1,
                               max_length=8,
                               validators=[validate_chars, validate_user_not_exists])
    password = forms.CharField(label='password',
                               min_length=1,
                               max_length=8,
                               validators=[validate_chars])


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username',
                               min_length=1,
                               max_length=8,
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
