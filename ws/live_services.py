from core.processing import release_bookings_by_timeout, delete_tickets_until
from init_data.set_data import set_settings
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


def init_default_properties(request):
    try:
        set_settings()
    except Exception:
        return HttpResponse(500)
    return HttpResponse(status=200)
