import datetime
from django.utils import timezone
from core.models import Ticket, TicketHistory, BuyAction
from .helpers import *


def book_ticket(user, ticket):
    timestamp = timezone.now()
    ticket.status = 'booked'
    ticket.booked_by = user
    ticket.booked = timestamp
    ticket.save()
    TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                 message=f'ticket {ticket.id} was booked {timestamp} by {user.username}')
    return ticket


def buy_ticket(user, ticket):
    if ticket is not None:
        timestamp = timezone.now()
        ticket.status = 'bought'
        ticket.bought_by = user
        ticket.bought = timestamp
        ticket.booked_by = None
        ticket.booked = None
        ticket.save()
        TicketHistory.objects.create(datetime=timestamp, ticket_id=ticket, user_id=user,
                                     message=f'ticket {ticket.id} was bought {timestamp} by {user.username}')
        return ticket


def buyback_ticket(user, ticket):
    if ticket is not None:
        if ticket.status == 'booked' and ticket.booked_by == user:
            return buy_ticket(user, ticket)


def release_booked_ticket(ticket, message='booked ticket was released'):
    if ticket is not None:
        ticket.status = 'available'
        ticket.booked_by = None
        ticket.booked = None
        ticket.save()
        TicketHistory.objects.create(datetime=timezone.now(), ticket_id=ticket, message=message)


def release_bookings_by_timeout():
    timestamp = timezone.now()
    timeout = int(get_app_property('booking_timeout'))
    tickets = Ticket.objects.filter(status='booked', booked__lte=timestamp - datetime.timedelta(minutes=timeout))
    for ticket in tickets:
        release_booked_ticket(ticket, f'booked ticket {ticket.id} was released due to timeout {timeout} minutes')


def clear_bookings(user, ticket_id):
    tickets = user.booked_tickets.filter(id=ticket_id)
    if len(tickets) > 0:
        release_booked_ticket(tickets[0], f'booked ticket was released by user {user.username}')


def check_credit_card(card_number, amount=0):
    cc = get_credit_card(card_number)
    if cc is None:
        return {'is_valid': False,
                'is_enough': False}
    else:
        if cc.amount < amount:
            return {'is_valid': True,
                    'is_enough': False}
        else:
            return {'is_valid': True,
                    'is_enough': True}


def save_payment(user, tickets, discount, init_price, final_price, info, is_lucky):
    r = BuyAction.objects.create(user=user,
                                 discount=discount,
                                 init_price=init_price,
                                 final_price=final_price,
                                 info=info,
                                 is_lucky=is_lucky)
    r.tickets.set(tickets)
    r.save()
    return r.id


def get_receipt(id):
    res = BuyAction.objects.filter(id=id)
    if len(res) != 0:
        return res[0]

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



def debit(user, credit_card, ticket, total_price, discount=None):
    if credit_card.amount < total_price:
        return False
        credit_card.amount -= total_price
        credit_card.save()
    if discount:
        discount.ticket_id = ticket
        discount.save()
    return True
