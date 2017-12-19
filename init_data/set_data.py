from core import processing
import datetime, random
from django.contrib.auth.models import User
from core.models import UserFeature, Feature

def set_settings():
    processing.set_app_property('max_book_ticket', '10')
    processing.set_app_property('user_buy_counter', '1')
    processing.set_app_property('user_buy_counter_limit', '10')
    processing.set_app_property('user_buy_counter_discount', '1')
    processing.set_app_property('user_logged_in_discount', '3')
    processing.set_app_property('snack_price', '50')
    processing.set_app_property('booking_timeout', '15')


def add_user_features():
    f1 = processing.add_feature('dog')[0]
    f2 = processing.add_feature('elephant')[0]
    f3 = processing.add_feature('clown')[0]
    UserFeature.objects.create(name='cat', price='50', incompatible_with=f1)
    UserFeature.objects.create(name='mouse', price='50', incompatible_with=f2)
    UserFeature.objects.create(name='parrot', price='50')


def add_discount_codes():
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);
    processing.add_discount_code(5);