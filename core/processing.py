import datetime, uuid
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Ticket, Performance, Feature, TicketHistory, Discount, AppSettings
from django.contrib.auth.models import User



def get_tickets(date_from=datetime.date.today(), date_to=datetime.date(datetime.MAXYEAR, 12, 31),
                time_from=datetime.time(hour=10), time_to=datetime.time(hour=22),
                price_from=0, price_to=9999999, features=[], description=''):
    if len(features) == 0:
        ff = Feature.objects.all()
        all_features = []
        for i in ff:
            all_features.append(i.feature)
    return Ticket.objects.filter(performance_id__date__gte=date_from,
                                 performance_id__date__lte=date_to,
                                 performance_id__time__gte=time_from,
                                 performance_id__time__lte=time_to,
                                 price__gte=price_from,
                                 price__lte=price_to,
                                 performance_id__description__contains=description,
                                 #TODO redo
                                 performance_id__feature__feature__in=features if len(features) != 0 else all_features
                                 ).order_by('performance_id__date', 'performance_id__time')


# this function returns tuple (object, bool)
def add_feature(feature_name):
    return Feature.objects.get_or_create(feature=feature_name)


def add_performance(date, time, description, features):
    res = Performance.objects.filter(date=date, time=time)
    if len(res) == 0:
        p = Performance(date=date, time=time, description=description)
        p.save()
        for feature in features:
            f = add_feature(feature)[0]
            p.feature_set.add(f)
        return p
    return res[0];


def add_tickets(performance, price, number=1):
    for i in range(number):
        Ticket.objects.create(status='available', price=price, performance_id=performance)


def delete_tickets_until(date=datetime.date.today(), time=datetime.datetime.now().time()):
    res = Performance.objects.filter(date__lte=date, time__lt=time)
    for perf in res:
        Ticket.objects.filter(performance_id=perf, status='available').delete()



def book_ticket(user, ticket):
    timestamp = datetime.datetime.now()
    ticket.status = 'booked'
    ticket.booked_by = user
    ticket.booked = timestamp
    ticket.save()
    TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                 message='ticket {0} was booked {1} by {2}'.
                                 format(ticket.id, timestamp, user.username))
    return ticket



def buy_ticket(user, ticket):
    timestamp = datetime.datetime.now()
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
        timestamp = datetime.datetime.now()
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
    tickets = Ticket.objects.filter(status='booked', booked__lte=timestamp-datetime.timedelta(minutes=15))
    timeout = get_app_property('booking_timeout')
    for ticket in tickets:


def get_closest_ticket():
    tickets = Ticket.objects.filter(status='available').order_by('performance_id__date', 'performance_id__time')
    return tickets[0]


def add_discount(code=str(uuid.uuid4()), percent=10):
    Discount.objects.create(code=code, percent=percent)


def get_total_price(user, ticket, discount=None, user_feature=None, snack=False):
    total = ticket.price
    if user_feature:
        total += user_feature.price
    if snack:
        total += float(get_app_property('snack_price'))
    total *= (100 - calculate_discount(user, discount))/100
    return total


def calculate_discount(user, discount):
    pass


def get_user_counter_discount():
    if get_app_property('user_buy_counter') == '0':
        return float(get_app_property('user_buy_counter_discount'))
    else:
        return 0


def debit(user, ticket, total_price):
    pass
    # if user.userdetails.amount < (total * (100 - discount.percent))/100:
    #     return False
    # user.userdetails.amount -= (ticket.price * (100 - discount.percent))/100
    # discount.ticket_id = ticket
    # discount.save()
    # user.userdetails.save()
    #
    # return True


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
        return ''