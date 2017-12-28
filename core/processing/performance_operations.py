import datetime
from django.db.models import Q, Count
from django.utils import timezone
from core.models import Ticket, Performance, Feature


def get_performances(date_from=timezone.now().date(), date_to=datetime.date.max,
                     time_from=datetime.time(hour=10), time_to=datetime.time(hour=22),
                     price_from=0, price_to=9999999, name='', description=''):
    date_from = date_from or datetime.date.today()
    date_to = date_to or datetime.date.max
    time_from = time_from or datetime.time(hour=10)
    time_to = time_to or datetime.time(hour=22)
    price_from = price_from if price_from is not None else 0
    price_to = price_to or 9999999

    perf_list = Performance.objects.annotate(tickets_count=Count('tickets')).filter(
        tickets_count__gt=0,
        date__gte=date_from,
        date__lte=date_to,
        time__gte=time_from,
        time__lte=time_to,
        price__gte=price_from,
        price__lte=price_to,
        name__contains=name,
        description__contains=description).order_by('date', 'time')
    for p in perf_list:
        if p.tickets.filter(status='available').count() > 0:
            yield p


def get_performance_simple(date_from, date_to, time_interval, price_interval, keyword):
    date_from = date_from or datetime.date.today()
    date_to = date_to or datetime.date.max
    if time_interval is not None:
        time_from = datetime.time(hour=int(time_interval[0]/60))
        time_to = datetime.time(hour=int(time_interval[1]/60))
    else:
        time_from = datetime.time(hour=10)
        time_to = datetime.time(hour=22)

    if price_interval is not None:
        price_from = price_interval[0]
        price_to = price_interval[1]
    else:
        price_from = 0
        price_to = 9999999

    perf_list = Performance.objects.annotate(tickets_count=Count('tickets')).filter(
        Q(name__contains=keyword) | Q(description__contains=keyword) | Q(features__feature=keyword),
        tickets_count__gt=0,
        date__gte=date_from,
        date__lte=date_to,
        time__gte=time_from,
        time__lte=time_to,
        price__gte=price_from,
        price__lte=price_to).order_by('date', 'time')

    for p in perf_list:
        if p.tickets.filter(status='available').count() > 0:
            yield p


# this function returns tuple (object, bool)
def add_feature(feature_name):
    ff = Feature.objects.filter(feature=feature_name.lower())
    if len(ff) == 0:
        f = Feature(feature=feature_name.lower())
        f.save()
        return f, True
    else:
        return ff[0], False


def get_performance(date, time):
    p = Performance.objects.filter(date=date, time=time)
    if len(p) != 0:
        return p[0]


def get_performance_by_id(id):
    p = Performance.objects.filter(id=id)
    if len(p) != 0:
        return p[0]


def update_performance(id, date, time, price, name, description, features):
    p = get_performance_by_id(id)
    if p is not None:
        p.date = date or p.date
        p.time = time or p.time
        p.price = price or p.price
        p.name = name or p.name
        p.description = description or p.description
        if features is not None:
            for f in features:
                feature = add_feature(f)[0]
                p.features.add(feature)
        else:
            p.features.clear()
        p.save()
        return p


def add_performance(date, time, price, name, description, features):
    res = get_performance(date=date, time=time)
    if res is None:
        p = Performance(date=date, time=time, price=price, name=name, description=description)
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
