from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from core import user_management, processing
from . import settings
import logging

# logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse('hello')


def login_view(request):
    if request.user.is_authenticated():
        return redirect(settings.BOOKING_URL)

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        action = request.POST['action']
        if username is None or password is None or action is None:
            return JsonResponse({'status': 'failed', 'message': 'one of mandatory fields not provided'}, status=400)

        result = user_management.validate_username(username)
        if not result[0]:
            return JsonResponse({'status': 'failed', 'message': result[1], 'field': 'username'}, status=400)

        result = user_management.validate_pass(password)
        if not result[0]:
            return JsonResponse({'status': 'failed', 'message': result[1], 'field': 'password'}, status=400)

        if action == 'login':
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': settings.BOOKING_URL}, status=200)
        if action == 'register':
            pass



def main(request):
    return render(request, 'booking.html')


@login_required(login_url=settings.LOGIN_URL)
def search_tickets_form(request):
    pass


@login_required(login_url=settings.LOGIN_URL)
def user_info(request):
    pass
