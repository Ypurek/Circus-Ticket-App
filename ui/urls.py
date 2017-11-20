"""circus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views, settings

urlpatterns = [
    path('', views.index, name='test'),
    path(settings.LOGIN_URL, views.auth_view, name='login'),
    path(settings.LOGOUT_URL, views.logout_view, name='logout'),
    path(settings.BOOKING_URL, views.booking, name='main'),
    path(settings.BOOK_URL, views.book, name='book'),
    path('user/', views.user_info)
]
