from django import forms
import re, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def check_if_array(self, value):
    if type(value) != list:
        raise ValidationError('Features provided not in list format', params={'value': value})


def check_if_array_contains_str(self, value):
    for x in value:
        if type(x) != str:
            raise ValidationError('feature not in string format', params={'value': x})


class ArrayField(forms.Field):
    def __init__(self, required=False, initial=[], widget=None, help_text=''):
        super().__init__()
        self.required = required
        self.initial = initial
        self.widget = widget
        self.help_text = help_text
        self.validators.append(check_if_array)
        self.validators.append(check_if_array_contains_str)

    def to_python(self, value):
        return value


class SearchTicketsForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField(required=False)
    price_from = forms.FloatField(required=False)
    price_to = forms.FloatField(required=False)
    description = forms.CharField(required=False)


class AddPerformanceForm(forms.Form):
    date = forms.DateField(label='date', input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    time = forms.TimeField(label='time')
    price = forms.FloatField(label='price',
                             min_value=1)
    description = forms.CharField(label='description')
    features = ArrayField()
    tickets_number = forms.IntegerField(label='tickets_number',
                                        min_value=1)



