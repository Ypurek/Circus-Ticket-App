from django.urls import path, include
from django.contrib import admin
from . import services

urlpatterns = [
    path('performances', services.performances)
    #path('performance/<int:id>', services.get_tickets)
]