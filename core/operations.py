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
    try:
        for perf_id, tickets in booking_list.items():
            t = int(tickets or 0)
            total += t
            p = get_performance_by_id(int(perf_id))
            available = p.tickets.filter(status='available').count()
            if t > available:
                return {'status': 'failed',
                        'message': f'cannot book more then available ({available}) for performance {p.name}'}
        already_booked = get_booked_tickets(user).count()
        booking_limit = int(get_app_property('max_book_ticket'))
        if total + already_booked > booking_limit:
            return {'status': 'failed',
                    'message': f'booking limit {booking_limit} exceeded. Already booked: {already_booked}'}

        for ticket in get_ticket_list_by_performance_ids(booking_list):
            book_ticket(user, ticket)
    except Exception:
        return {'status': 'failed',
                'message': 'booking failed due to backend reason like type casting or db access'}
    return {'status': 'success',
            'message': f'{total} tickets added to cart'}


def get_ticket_list_by_performance_ids(booking_list):
    ticket_list = []
    for perf_id, tickets in booking_list.items():
        p = get_performance_by_id(int(perf_id))
        ticket_list.extend(p.tickets.filter(status='available')[:int(tickets or 0)])
    return ticket_list


def bulk_release(user, booking_list):
    for ticket_id, checked in booking_list.items():
        if type(checked) == bool:
            if checked:
                try:
                    clear_bookings(user, int(ticket_id or 0))
                except:
                    return {'status': 'failed',
                            'message': 'booking failed due to backend reason like type casting or db access'}
        else:
            return {'status': 'failed',
                    'message': f'request data incorrect for pair ({ticket_id}: {checked}'}

    return {'status': 'success',
            'message': 'selected tickets released'}


def prepare_invoice(user, tickets_list, discount_coupon=None):
    total_price = 0
    user_dis = int(get_app_property('user_logged_in_discount')) if user.username != 'anonymous' else 0
    # coupon_dis = 0 if discount_coupon is None else discount_coupon.percent

    for ticket in tickets_list:
        total_price += ticket.performance.price

    total_discount = user_dis  # if user_dis > coupon_dis else coupon_dis
    final_price = total_price * (100 - total_discount) / 100

    return {'total_price': total_price,
            'total_discount': total_discount,
            'final_price': final_price}


def update_invoice(user, updates_list):
    result = {}
    tickets = {}
    total_price = 0
    snack_price = int(get_app_property('snack_price'))
    for ticket_id, snack in updates_list['snacks'].items():
        ticket = get_ticket(ticket_id)
        price = ticket.performance.price
        pet = get_user_feature(updates_list['pets'][ticket_id])
        pet_price = 0
        if pet is not None:
            if pet.incompatible_with in ticket.performance.features.all():
                return {'status': 'failed',
                        'message': f'customer cannot take {pet.name} to performance {ticket.performance.name}',
                        'ticket_id': ticket.id}
            pet_price = pet.price
        if snack:
            price += snack_price
        tickets[ticket_id] = price + pet_price
        total_price += price + pet_price
    result['tickets'] = tickets
    result['totalPrice'] = total_price

    coupon_dis = get_discount(updates_list['coupon'])
    user_dis = int(get_app_property('user_logged_in_discount')) if user.username != 'anonymous' else 0
    total_discount = user_dis if user_dis > coupon_dis else coupon_dis
    result['couponStatus'] = coupon_dis != 0
    result['totalDiscount'] = total_discount
    result['finalPrice'] = total_price * (100 - total_discount) / 100
    return result


def debit(user, price, discount, credit_card, tickets_list, discount_code, info):
    ticket_links = []
    for ticket in tickets_list:
        ticket_links.append(ticket)
        buy_ticket(user, ticket)
    lucky = get_user_counter_discount()
    credit_card.amount -= price * (100 - discount - lucky) / 100
    credit_card.save()
    d = Discount.objects.filter(code=discount_code)
    if len(d) > 0:
        d[0].used = True
        d[0].save()
    receipt_id = save_payment(user=user,
                              tickets=ticket_links,
                              discount=discount + lucky,
                              init_price=price,
                              final_price=price * (100 - discount - lucky) / 100,
                              info=info,
                              is_lucky=lucky > 0)
    increment_user_counter_discount()
    return receipt_id


def get_ticket_list(input_dict):
    result = []
    for k, v in input_dict:
        result.append(get_ticket(k))
    return result
