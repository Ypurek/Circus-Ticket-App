from django.urls import path, include
from . import services, live_services

urlpatterns = [
    path('auto/remove_old', live_services.remove_old_tickets),
    path('auto/release', live_services.release_bookings),
    path('auto/clear', live_services.release_bookings),

    path('performances', services.performances),
    path('performance/<int:id>', services.performance),
    path('tickets', services.tickets),
    path('ticket/<int:id>', services.ticket),
    path('properties', services.get_properties),
]
