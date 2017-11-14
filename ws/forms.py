from django import forms
from django.core.exceptions import ValidationError


def check_if_array(value):
    if type(value) != list:
        raise ValidationError('Features provided not in list format', params={'value': value})


def check_if_array_contains_str(value):
    for x in value:
        if type(x) != str:
            raise ValidationError('feature not in string format', params={'value': x})


class ArrayField(forms.Field):
    def __init__(self, required=False, initial=[], widget=None, help_text='', label=''):
        self.default_validators = [check_if_array, check_if_array_contains_str]
        super().__init__(required=required, initial=initial, widget=widget, help_text=help_text, label=label)

    def clean(self, value):
        return super().clean(value)


class SearchTicketsForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField(required=False)
    price_from = forms.FloatField(required=False)
    price_to = forms.FloatField(required=False)
    description = forms.CharField(required=False)


class AddPerformanceForm(forms.Form):
    date = forms.DateField(input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    time = forms.TimeField(label='time')
    price = forms.FloatField(label='price', min_value=1)
    description = forms.CharField(label='description')
    features = ArrayField(label='features')
    ticketsNumber = forms.IntegerField(label='ticketsNumber', min_value=1)



