import datetime
from .models import Ticket, Performance, Feature, TicketHistory
from django.contrib.auth.models import User


def get_all_tickets_by(date):
    return Ticket.objects.filter(date__gte=datetime.date.today(), date__lt=date)


def get_all_tickets_by(date, time):
    return get_all_tickets_by(date).filter(time=time)


def get_tickets(date_from=datetime.date.today(), date_to=datetime.MAXYEAR, time_from=datetime.datetime.now().time(),
                time_to=datetime.time(hour=23), price_from=0, price_to=9999999, features=[], description=''):
    return Ticket.objects.filter(performance_id__date__gte=date_from,
                                 performance_id__date__lte=date_to,
                                 performance_id__time__gte=time_from,
                                 performance_id__time__lte=time_to,
                                 price__gte=price_from,
                                 price__lte=price_to,
                                 performance_id__description__contains=description,
                                 performance_id__feature__feature__in=features
                                 )


def add_feature(feature_name):
    return Feature.objects.get_or_create(feature=feature_name)


def add_performance(date, time, description, features):
    res = Performance.objects.filter(date=date, time=time)
    if len(res) == 0:
        p = Performance(date=date, time=time, description=description)
        p.save()
        for feature in features:
            f = add_feature(feature)
            p.feature_set.add(f)
        return p
    return res[0];


def add_tickets(performance, price, number=1):
    for i in range(number):
        Ticket.objects.create(status='available', price=price, performance_id=performance)


def add_tickets(date, time, price, number=1):
    res = Performance.objects.filter(date=date, time=time)
    if len(res) != 0:
        for i in range(number):
            add_tickets(res[0], price, number=1)
        return Ticket.objects.filter(performance_id=res[0])


def delete_tickets_until(date=datetime.date.today(), time=datetime.datetime.now().time()):
    res = Performance.objects.filter(date__lte=date, time__lt=time)
    for perf in res:
        Ticket.objects.filter(performance_id=perf, status='available').delete()


def book_ticket(user, date, time):
    perf = Performance.objects.filter(date=date, time=time)
    tickets = Ticket.objects.filter(performance_id=perf[0], status='available')
    if len(perf) != 0:
        timestamp = datetime.datetime.now()
        tickets[0].status = 'booked'
        tickets[0].booked_by = user
        tickets[0].booked = timestamp
        tickets[0].save()
        TicketHistory.objects.create(datetime=timestamp, ticket_id=tickets[0], user_id=user,
                                     message='ticket {0} was booked {1} by {2}'.
                                     format(tickets[0].id, timestamp, user.username))
        return tickets[0]


def buy_ticket(user, date, time):
    perf = Performance.objects.filter(date=date, time=time)
    tickets = Ticket.objects.filter(performance_id=perf[0], status__in=('available', 'booked'))
    if len(perf) != 0:
        timestamp = datetime.datetime.now()
        tickets[0].status = 'bought'
        tickets[0].bought_by = user
        tickets[0].bought = timestamp
        tickets[0].save()
        TicketHistory.objects.create(datetime=timestamp, ticket_id=tickets[0], user_id=user,
                                     message='ticket {0} was bought {1} by {2}'.
                                     format(tickets[0].id, timestamp, user.username))
        return tickets[0]


def get_time_diff(time1, time2):
    return abs((time1.hour * 60 + time1.minute) - (time2.hour * 60 + time2.minute))


def release_bookings():
    tickets = Ticket.objects.filter(status='booked')
    timestamp = timestamp = datetime.datetime.now();
    for ticket in tickets:
        if get_time_diff(timestamp.time(), ticket.booked_by) >= 15:
            ticket.status = 'available'
            ticket.booked_by = None
            ticket.booked = None
            ticket.save()
            TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket,
                                         message='ticket {0} was released {1} by timeout'.
                                         format(tickets[0].id, timestamp))
