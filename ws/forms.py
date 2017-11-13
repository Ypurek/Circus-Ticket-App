from django import forms
import re, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SearchTicketsForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField(required=False)
    price_from = forms.FloatField(required=False)
    price_to = forms.FloatField(required=False)
    text = forms.CharField(required=False)





