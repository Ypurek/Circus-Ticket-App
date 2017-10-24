from django import forms
import re
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # TODO add validators
    # https://docs.djangoproject.com/en/1.11/ref/validators/
    username = forms.CharField(label='username', min_length=1, max_length=8,validators=[],error_messages='')
    password = forms.CharField(label='password', min_length=1, max_length=8)
    action = forms.CharField(label='action')

    def validate_chars(self, value):
        if not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=value):
            raise forms.ValidationError('username contains invalid characters')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=username):
            raise forms.ValidationError('username contains invalid characters')
        elif not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=password):
            raise forms.ValidationError('password contains invalid characters')
        elif not len(User.objects.filter(username=username)) == 1:
            raise forms.ValidationError('user does not exist')
        elif not len(User.objects.filter(username=username, password=password)) == 1:
            raise forms.ValidationError('wrong password')
        return self.cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', min_length=1, max_length=8)
    password = forms.CharField(label='password', min_length=1, max_length=8)
    action = forms.CharField(label='action')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=username):
            raise forms.ValidationError('username contains invalid characters')
        elif not re.match(pattern='^[a-zA-Z0-9]{1,8}$', string=password):
            raise forms.ValidationError('password contains invalid characters')
        return self.cleaned_data
