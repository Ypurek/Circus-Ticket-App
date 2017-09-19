from django.contrib.auth.models import User
from .models import UserDetails


def register(username, password):
    pass


def login(username, password):
    pass


def add_details(user, email, birth_day, image, amount=1000):
    # TODO email validation
    user.email = email
    user.userdetails.birth_day = birth_day
    user.userdetails.image = image
    user.userdetails.amount = amount
    user.save()
    user.userdetails.save()
