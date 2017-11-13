from django.urls import path, include
from django.contrib import admin
from . import services

urlpatterns = [
    path('tickets', services.get_tickets())
]