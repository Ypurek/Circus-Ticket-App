from .processing import *


def performance_to_json(performance):
    feature_list = []
    for feature in performance.features.filter():
        feature_list.append(feature.feature)
    return {'id': performance.id,
            'date': performance.date,
            'time': performance.time,
            'name': performance.name,
            'description': performance.description,
            'price': performance.price,
            'features': feature_list,
            'ticketsNumber': performance.tickets.filter(status='available').count()}


def ticket_to_json(ticket):
    result = {'id': ticket.id,
              'performance': {'id': ticket.performance.id,
                              'name': ticket.performance.name},
              'status': ticket.status}
    if ticket.booked is not None:
        result['booked'] = ticket.booked
    if ticket.bought is not None:
        result['bought'] = ticket.bought
    if ticket.booked_by is not None:
        result['booked_by'] = ticket.booked_by.username
    if ticket.bought_by is not None:
        result['bought_by'] = ticket.bought_by.username
    return result


def bulk_book(booking_list):
    total = 0
    for perf_id, tickets in booking_list.items():
        total += tickets
    if total <= get_app_property('max_book_ticket'):
        for perf_id, tickets in booking_list.items():
            p = get_performance_by_id(int(perf_id))
            if p.tickets.filter(status='available'):
                pass


