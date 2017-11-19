from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from core import user_management, processing, operations
from . import settings
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.template import loader
import json
from core.forms import GetPerformanceForm


def normalize_url(url):
    if not url.startswith('/'):
        return '/' + url
    else:
        return url


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
                    return JsonResponse({'status': 'success', 'redirect_url': normalize_url(settings.BOOKING_URL)},
                                        status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': {'username': 'such user does not exist'}},
                                        status=400)
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
                return JsonResponse({'status': 'success', 'redirect_url': normalize_url(settings.BOOKING_URL)},
                                    status=200)
            else:
                return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
        if action == 'anonymous':
            user = authenticate(request,
                                username=settings.ANONYMOUS['username'],
                                password=settings.ANONYMOUS['password'])
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': normalize_url(settings.BOOKING_URL)}, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': 'bad action'}, status=400)


def main(request):
    return render(request, 'booking.html')


@login_required(login_url=settings.LOGIN_URL)
def booking(request):
    context = {'performance_list': [],
               'display_search_results': 'None'}

    if request.method == 'GET':
        form = GetPerformanceForm()

    if request.method == 'POST':
        form = GetPerformanceForm(request.POST)
        if form.is_valid():
            context['form'] = form
            context['display_search_results'] = ''
            perf_list = processing.get_performances(date_from=form.cleaned_data['date_from'],
                                                    date_to=form.cleaned_data['date_to'],
                                                    time_from=form.cleaned_data['time_from'],
                                                    time_to=form.cleaned_data['time_to'],
                                                    price_from=form.cleaned_data['price_from'],
                                                    price_to=form.cleaned_data['price_to'],
                                                    name=form.cleaned_data['name'],
                                                    description=form.cleaned_data['description'])
            for performance in perf_list:
                context['performance_list'].append(operations.performance_to_json(performance))

    context['form'] = form
    return render(request, 'booking.html', context)


@login_required(login_url=settings.LOGIN_URL)
def book(request):
    pass


@login_required(login_url=settings.LOGIN_URL)
def buy(request):
    pass


@login_required(login_url=settings.LOGIN_URL)
def user_info(request):
    context = {'user': request.user,
               'tickets_list': []}

    if request.method == 'GET':
        context['tickets_list'] = request.user.booked_tickets.filter()

    if request.method == 'POST':
            pass

    return render(request, 'user_info.html', context)