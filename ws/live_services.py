from core.processing import release_bookings_by_timeout, delete_tickets_until, clear_ticket_history
from core.processing.workflow import clear_discount_codes, clear_credit_cards
from django.http import HttpResponse


def release_bookings(request):
    try:
        release_bookings_by_timeout()

    except Exception:
        return HttpResponse(500)
    return HttpResponse(status=200)


def remove_old_tickets(request):
    try:
        delete_tickets_until()
    except Exception:
        return HttpResponse(500)
    return HttpResponse(status=200)


def clear(request):
    try:
        clear_ticket_history()
        clear_discount_codes()
        clear_credit_cards()
    except Exception:
        return HttpResponse(500)
    return HttpResponse(status=200)
