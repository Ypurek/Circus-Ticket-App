from django.contrib import admin
from .models import BugRegister

# Register your models here.
# admin.site.register(BugRegister)


@admin.register(BugRegister)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'isActive')
    search_fields = ('name',)
    ordering = ('name',)