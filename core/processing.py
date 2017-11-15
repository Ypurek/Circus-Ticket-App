import datetime, uuid, re, random
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Ticket, Performance, Feature, TicketHistory, Discount, AppSettings, CreditCard
from .exceptions import AppPropertyNotSet
from django.contrib.auth.models import User


def get_performances(date_from=timezone.now().date(), date_to=datetime.date.max,
                     time_from=datetime.time(hour=10), time_to=datetime.time(hour=22),
                     price_from=0, price_to=9999999, description=''):
    return Performance.objects.filter(date__gte=date_from,
                                      date__lte=date_to,
                                      time__gte=time_from,
                                      time__lte=time_to,
                                      price__gte=price_from,
                                      price__lte=price_to,
                                      description__contains=description).order_by('date', 'time')


# this function returns tuple (object, bool)
def add_feature(feature_name):
    return Feature.objects.get_or_create(feature=feature_name.lower())


def get_performance(date, time):
    p = Performance.objects.filter(date=date, time=time)
    if len(p) != 0:
        return p[0]


def get_performance_by_id(id):
    p = Performance.objects.filter(id=id)
    if len(p) != 0:
        return p[0]


def update_performance(id, date, time, price, description, features):
    p = get_performance_by_id(id)
    if p is not None:
        p.date = date or p.date
        p.time = time or p.time
        p.price = price or p.price
        p.description = description or p.description
        p.features.set(features if features is not None else [])
        p.save()
        return p


def add_performance(date, time, price, description, features):
    res = get_performance(date=date, time=time)
    if res is None:
        p = Performance(date=date, time=time, price=price, description=description)
        p.save()
        for feature in features:
            f = add_feature(feature)[0]
            p.features.add(f)
        return p
    else:
        return res


def add_tickets(performance, number=1):
    for i in range(number):
        Ticket.objects.create(status='available', performance=performance)


def get_tickets():
    return Ticket.objects.filter()


def delete_tickets_until(date=timezone.now().date(), time=timezone.now().time()):
    res = Performance.objects.filter(date__lte=date, time__lt=time)
    for perf in res:
        Ticket.objects.filter(performance=perf, status='available').delete()


def book_ticket(user, ticket):
    timestamp = timezone.now()
    ticket.status = 'booked'
    ticket.booked_by = user
    ticket.booked = timestamp
    ticket.save()
    TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                 message='ticket {0} was booked {1} by {2}'.
                                 format(ticket.id, timestamp, user.username))
    return ticket


def buy_ticket(user, ticket):
    timestamp = timezone.now()
    ticket.status = 'bought'
    ticket.bought_by = user
    ticket.bought = timestamp
    ticket.save()
    TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                 message='ticket {0} was bought {1} by {2}'.

                                 format(ticket.id, timestamp, user.username))
    return ticket


def buyback_ticket(user, ticket):
    if ticket.status == 'booked' and ticket.booked_by == user:
        timestamp = timezone.now()
        ticket.status = 'bought'
        ticket.bought_by = user
        ticket.bought = timestamp
        ticket.save()
        TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                     message='ticket {0} was bought {1} by {2}'.
                                     format(ticket.id, timestamp, user.username))
        return ticket


def release_bookings():
    timestamp = timezone.now()
    timeout = int(get_app_property('booking_timeout'))
    tickets = Ticket.objects.filter(status='booked', booked__lte=timestamp - datetime.timedelta(minutes=timeout))
    for ticket in tickets:
        ticket.status = 'available'
        ticket.booked_by = None
        ticket.booked = None
        ticket.save()
        TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket,
                                     message='booked ticket {0} was released due to timeout {1} minutes'.
                                     format(ticket.id, timeout))


def get_closest_ticket():
    tickets = Ticket.objects.filter(status='available').order_by('performance__date', 'performance__time')
    return tickets[0]


def add_discount_code(percent=5, code=str(uuid.uuid4())):
    return Discount.objects.create(code=code, percent=percent)


def get_total_price(ticket, is_user=False, discount_code=None, user_feature=None, snack=False):
    total = ticket.performance.price
    if user_feature:
        total += user_feature.price
    if snack:
        total += float(get_app_property('snack_price'))
    total *= (100 - calculate_final_discount(discount_code, is_user)) / 100
    return total


def calculate_final_discount(discount_code, is_user):
    tup = get_discount_parts(discount_code, is_user)
    return (tup[0][1] if tup[0][1] > tup[1][1] else tup[1][1]) + tup[2][1]


def get_discount_parts(discount_code, is_user=False):
    discount_dis = discount_code.percent if discount_code else 0
    user_dis = get_app_property('user_logged_in_discount') if is_user else 0
    return (('discount by code', discount_dis),
            ('discount for authenticated users', int(user_dis)),
            ('random discount', get_user_counter_discount()))


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


def debit(user, credit_card, ticket, total_price, discount=None):
    if credit_card.amount < total_price:
        return False
        credit_card.amount -= total_price
        credit_card.save()
        increment_user_counter_discount()
    if discount:
        discount.ticket_id = ticket
        discount.save()
    return True


def check_discount_code(code):
    dis = Discount.objects.filter(code=code, ticket_id=None)
    if len(dis) == 0:
        return False
    else:
        return True


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


def check_new_credit_card_number(card_number):
    same = CreditCard.objects.filter(card_number=card_number)
    if re.compile('^\d{4} \d{4} \d{4} \d{4}$').fullmatch(card_number) and len(same) == 0:
        return True
    else:
        return False


def add_credit_card(card_number, amount=1000):
    return CreditCard.objects.create(card_number=card_number, amount=amount)


def generate_credit_cards(number=1, amount=1000):
    c = 0
    while c < number:
        card_number = ''
        for i in range(4):
            card_number += f'{random.randint(0, 9999):04} '
        if check_new_credit_card_number(card_number.strip()):
            add_credit_card(card_number, amount)
            c += 1


def get_credit_card_assignments(card_number):
    cards = CreditCard.objects.filter(card_number=card_number)
    if len(cards) > 0:
        card = cards[0]
    return card.user_set()
