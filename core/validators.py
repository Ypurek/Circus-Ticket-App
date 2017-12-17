import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models


def is_credit_card(value):
    if not re.match(pattern='^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$', string=value):
        raise ValidationError('invalid credit card number', params={'value': value})


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


def validate_credit_card_exists(value):
    cc = models.CreditCard.objects.filter(card_number=value)
    if len(cc) == 0:
        raise ValidationError('credit card does not exists', params={'value': value})

