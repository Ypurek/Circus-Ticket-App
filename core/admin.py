from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ticket)
admin.site.register(UserDetails)
admin.site.register(Performance)
admin.site.register(Feature)
admin.site.register(Discount)
admin.site.register(TicketHistory)
