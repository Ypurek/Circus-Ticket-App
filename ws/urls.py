from django.urls import path, include
from . import services, live_services

urlpatterns = [
    path('auto/cleanup', live_services.remove_old_tickets),
    path('auto/release', live_services.release_bookings),

    path('performances', services.performances),
    path('performance/<int:id>', services.performance),
    path('tickets', services.tickets)
]