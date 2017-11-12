from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from core import user_management, processing
from . import settings
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User


def index(request):
    return HttpResponse('hello')


def auth_view(request):
    if request.user.is_authenticated:
        return redirect(settings.BOOKING_URL)

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        action = request.POST['action']

        if action == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request,
                                    username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return JsonResponse({'status': 'success', 'redirect_url': normilize_url(settings.BOOKING_URL)}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': {'username':'such user does not exist'}}, status=400)
            else:
                return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
        if action == 'register':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                User.objects.create_user(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password'])
                user = authenticate(request,
                                    username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                login(request, user)
                return JsonResponse({'status': 'success', 'redirect_url': normilize_url(settings.BOOKING_URL)}, status=200)
            else:
                return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
        if action == 'anonymous':
            user = authenticate(request,
                                username=settings.ANONYMOUS['username'],
                                password=settings.ANONYMOUS['password'])
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': normilize_url(settings.BOOKING_URL)}, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': 'bad action'}, status=400)


def main(request):
    return render(request, 'booking.html')


@login_required(login_url=settings.LOGIN_URL)
def search_tickets_form(request):
    pass


@login_required(login_url=settings.LOGIN_URL)
def user_info(request):
    pass


def normilize_url(url):
    if not url.startswith('/'):
        return '/' + url
    else:
        return url