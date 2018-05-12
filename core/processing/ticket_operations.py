import datetime
from django.utils import timezone
from core.models import Ticket, TicketHistory
from django.db.models import Q


def get_ticket(id):
    t = Ticket.objects.filter(id=int(id))
    if len(t) == 1:
        return t[0]


def get_tickets():
    return Ticket.objects.all()


def get_booked_tickets(user):
    return user.booked_tickets.filter(performance__date__gte=timezone.now().date())


def get_bought_tickets(user):
    return user.bought_tickets.all()


def delete_tickets_until(date=timezone.now().date(), time=timezone.now().time()):
    Ticket.objects.filter(Q(status='available') | Q(status='booked'),
                          performance__date__lte=date,
                          performance__time__lt=time).delete()


def delete_ticket(id):
    Ticket.objects.filter(status='available', id=id).delete()
    if len(Ticket.objects.filter(id=id)) == 0:
        return True
    else:
        False


def get_ticket_history():
    return TicketHistory.objects.all().order_by('-id')
