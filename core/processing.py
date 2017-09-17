import datetime
from django.utils import timezone
from .models import Ticket, Performance, Feature


def get_all_tickets(date):
    return Ticket.objects.filter(date__gte=datetime.date.today(), date__lt=date)


def get_all_tickets(date, time):
    return get_all_tickets(date).filter(time=time)
    a = null


def delete_outdated_tickets():
    Ticket.objects.filter(date__lte=datetime.date.today(), time__lt=timezone.now(), status='available').delete()


def get_tickets(date_from=datetime.date.today(), date_to=datetime.MAXYEAR, time_from=timezone.now(),
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