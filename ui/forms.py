from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_chars(value):
    if not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=value):
        raise ValidationError('Field contains invalid characters', params={'value': value})


def validate_user_exists(value):
    res = User.objects.filter(username=value)
    if len(res) != 0:
        raise ValidationError('user already exists', params={'value': value})


def validate_user_not_exists(value):
    res = User.objects.filter(username=value)
    if len(res) == 0:
        raise ValidationError('user does not exist', params={'value': value})


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
