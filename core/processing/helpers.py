import uuid, re, random
from core.models import AppSettings, Discount, CreditCard, UserFeature
from core.exceptions import AppPropertyNotSet


# Properties
def set_app_property(key, value):
    prop = AppSettings.objects.filter(property=key)
    if len(prop) == 0:
        AppSettings.objects.create(property=key, value=value)
    else:
        prop[0].value = value
        prop[0].save()


def get_app_property(key):
    prop = AppSettings.objects.filter(property=key)
    if len(prop) != 0:
        return prop[0].value
    else:
        raise AppPropertyNotSet(message='property {0} not set'.format(key))


# Discounts
def generate_discount_code(percent=5, code=''):
    if len(code) == 0:
        code = str(uuid.uuid4())
    return Discount.objects.create(code=code, percent=percent)


def get_discount(code):
    d = Discount.objects.filter(code=code, used=False)
    if len(d) == 0:
        return 0
    else:
        return d[0].percent


def check_discount_code(code):
    dis = Discount.objects.filter(code=code, used=False)
    if len(dis) == 0:
        return False
    else:
        return True


def get_discounts_list():
    return Discount.objects.filter(used=False).values()


def get_user_counter_discount():
    if get_app_property('user_buy_counter') == '0':
        return int(get_app_property('user_buy_counter_discount'))
    else:
        return 0


def increment_user_counter_discount():
    limit = int(get_app_property('user_buy_counter_limit'))
    current = int(get_app_property('user_buy_counter'))
    dis = (current + 1) % limit
    set_app_property('user_buy_counter', str(dis))


# Features
def get_user_features_list():
    return UserFeature.objects.all()


def get_user_feature(feature_name):
    f = UserFeature.objects.filter(name=feature_name)
    if len(f) == 1:
        return f[0]


# Credit Cards
def check_new_credit_card_number(card_number):
    same = CreditCard.objects.filter(card_number=card_number)
    if re.compile('^\d{4} \d{4} \d{4} \d{4}$').fullmatch(card_number) and len(same) == 0:
        return True
    else:
        return False


def get_credit_card_list():
    return CreditCard.objects.all().values()


def add_credit_card(card_number, amount=1000):
    return CreditCard.objects.create(card_number=card_number, amount=amount)


def get_credit_card(card_number):
    cc = CreditCard.objects.filter(card_number=card_number)
    if len(cc) == 1:
        return cc[0]


def add_credit_card(card_number, amount=1000):
    return CreditCard.objects.create(card_number=card_number, amount=amount)


def generate_credit_cards(amount=1000):
    card_number = ''
    for i in range(4):
        card_number += f'{random.randint(0, 9999):04} '
    CreditCard.objects.create(card_number=card_number.strip(), amount=amount)
