from django.contrib.auth.models import User
from .models import Profile


def register(username, password):
    pass


def login(username, password):
    pass


def validate_username(username):
    return True, 'success'


def validate_pass(password):
    return True, 'success'


def add_details(user, email, birth_day, image, amount=1000):
    # TODO email validation
    user.email = email
    user.userdetails.birth_day = birth_day
    user.userdetails.image = image
    user.userdetails.amount = amount
    user.save()
    user.userdetails.save()
