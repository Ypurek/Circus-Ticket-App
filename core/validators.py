import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models


def is_credit_card(value):
    if not re.match(pattern='^\d{4} \d{4} \d{4} \d{4}$', string=value):
        raise ValidationError('invalid credit card number', params={'value': value})


def is_credit_card_unique(value):
    cards = models.CreditCard.objects.filter(card_number=value)
    if len(cards) > 0:
        raise ValidationError('such card number already exists', params={'value': value})


def validate_chars(value):
    if not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=value):
        raise ValidationError('field contains invalid characters', params={'value': value})


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


def is_feature_unique(value):
    ff = models.Feature.objects.filter(feature=value)
    if len(ff) > 0:
        raise ValidationError('such feature already exists', params={'value': value})

