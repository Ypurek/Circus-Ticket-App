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


def bulk_book(user, booking_list):
    total = 0
    for perf_id, tickets in booking_list.items():
        total += tickets
        p = get_performance_by_id(int(perf_id))
        available = p.tickets.filter(status='available').count()
        if tickets > available:
            return {'status': 'failed',
                    'message': f'cannot book more then available ({available}) for performance {p.name}'}

    already_booked = get_booked_tickets(user)
    booking_limit = get_app_property('max_book_ticket')

    if total + already_booked > booking_limit:
        return {'status': 'failed',
                'message': f'cannot book more tickets then booking limit {booking_limit} allows'}

    for perf_id, tickets in booking_list.items():
        p = get_performance_by_id(int(perf_id))
        ticket_list = p.tickets.filter(status='available')[:tickets]
        for ticket in ticket_list:
            book_ticket(user, ticket)

    return {'status': 'success',
            'message': f'{total} tickets added to cart'}






