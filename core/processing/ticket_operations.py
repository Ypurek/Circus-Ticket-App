from django.utils import timezone
from core.models import Ticket, TicketHistory


def get_ticket(id):
    t = Ticket.objects.filter(id=int(id))
    if len(t) == 1:
        return t[0]


def get_tickets():
    return Ticket.objects.all()


def get_booked_tickets(user):
    return user.booked_tickets.all()


def get_bought_tickets(user):
    return user.bought_tickets.all()


def delete_tickets_until(date=timezone.now().date(), time=timezone.now().time()):
    Ticket.objects.filter(performance__date__lte=date,
                          performance__time__lt=time,
                          status='available').delete()


def get_closest_ticket():
    tickets = Ticket.objects.filter(status='available').order_by('performance__date', 'performance__time')
    return tickets[0]


def get_ticket_history():
    return TicketHistory.objects.all()
