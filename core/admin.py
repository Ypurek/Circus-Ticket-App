from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Feature)
admin.site.register(TicketHistory)
admin.site.register(BuyAction)


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('property', 'value')
    search_fields = ('property',)
    ordering = ('property',)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'price')
    search_fields = ('name', 'description')
    list_filter = ('date', 'time')
    ordering = ('date', 'time')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('status', 'performance', 'booked', 'bought', 'booked_by', 'bought_by')
    search_fields = ('status', 'booked_by', 'bought_by')
    list_filter = ('status', 'booked_by', 'bought_by')
    ordering = ('status',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent', 'used')
    search_fields = ('code',)
    ordering = ('code',)


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'amount')
    search_fields = ('card_number',)
    ordering = ('card_number',)


@admin.register(UserFeature)
class UserFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'incompatible_with')
    search_fields = ('name',)
    ordering = ('name',)