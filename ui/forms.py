from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=8)
    password = forms.CharField(label='password', max_length=8)
    action = forms.CharField(label='action')
