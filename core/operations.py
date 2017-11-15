def performance_to_json(performance):
    feature_list = []
    for feature in performance.features.filter():
        feature_list.append(feature.feature)
    return {'id': performance.id,
            'date': performance.date,
            'time': performance.time,
            'description': performance.description,
            'price': performance.price,
            'features': feature_list,
            'ticketsNumber': performance.tickets.filter(status='available').count()}


def ticket_to_json(ticket):
    result = {'id': ticket.id,
              'performanceID': ticket.performance.id,
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


