from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseNotAllowed, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, login, logout
from .forms import EditableUserInfo
from core import user_management, processing, operations
from . import settings
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
import json
from core.forms import GetPerformanceForm


def normalize_url(url):
    if not url.startswith('/'):
        return '/' + url
    return url


def index(request):
    if request.user.is_authenticated:
        return redirect(normalize_url(settings.BOOKING_URL))
    else:
        return redirect(normalize_url(settings.LOGIN_URL))


def auth_view(request):
    if request.user.is_authenticated:
        return redirect(normalize_url(settings.BOOKING_URL))

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
            return JsonResponse({'status': 'success', 'redirect_url': normalize_url(settings.BOOKING_URL)}, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': 'bad action'}, status=400)


def logout_view(request):
    logout(request)
    return redirect(normalize_url(settings.LOGIN_URL))


def booking(request):
    context = {'user': request.user,
               'performance_list': [],
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


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def book(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        result = operations.bulk_book(user=request.user, booking_list=body)
        if result['status'] == 'success':
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def clear_bookings(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        result = operations.bulk_release(user=request.user, booking_list=body)
        if result['status'] == 'success':
            return JsonResponse(result, status=202)
        else:
            return JsonResponse(result, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def buy(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # TODO override error messages on buy tickets
        result = operations.bulk_book(user=request.user, booking_list=body)
        if result['status'] == 'success':
            result['redirect_url'] = settings.BUY_INFO_URL
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def buy_back(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success',
                             'redirect_url': settings.BUY_INFO_URL}, status=200)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def buy_info(request):
    tickets = request.user.booked_tickets.all()
    if len(tickets) == 0:
        return redirect(normalize_url(settings.BOOKING_URL))

    context = {'user': request.user,
               'tickets': request.user.booked_tickets.all(),
               'stats': operations.prepare_invoice(request.user, request.user.booked_tickets.all()),
               'discounts': {'user_buy_counter_discount': processing.get_app_property('user_buy_counter_discount'),
                             'user_buy_counter_limit': processing.get_app_property('user_buy_counter_limit')},
               'features': processing.get_user_features_list()}
    # if request.user.username != 'anonymous':
    #     disc = context['discounts'] = processing.get_app_property('user_logged_in_discount')

    return render(request, 'buy.html', context)


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def user_info(request):
    context = {'user': request.user,
               'booked_tickets_list': [],
               'bought_tickets_list': []}

    if request.method == 'GET':
        context['booked_tickets_list'] = request.user.booked_tickets.filter()
        context['bought_tickets_list'] = request.user.bought_tickets.filter()

    if request.method == 'POST':
        pass

    return render(request, 'user_info.html', context)


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def check_credit_card(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        result = processing.check_credit_card(card_number=body['credit_card'],
                                              amount=body['amount'])
        return JsonResponse(result, status=200)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def update_price(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        result = operations.update_invoice(user=request.user, updates_list=body)
        if result.get('status') is not None:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=200)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def process_payment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        payment_info = operations.update_invoice(user=request.user, updates_list=body)
        cc = processing.check_credit_card(card_number=body['creditCard'],
                                          amount=payment_info['finalPrice'])

        if cc['is_valid']:
            if cc['is_enough']:
                receipt_id = operations.debit(user=request.user,
                                              price=payment_info['totalPrice'],
                                              discount=payment_info['totalDiscount'],
                                              credit_card=processing.get_credit_card(body['creditCard']),
                                              tickets_list=request.user.booked_tickets.all(),
                                              discount_code=body['coupon'],
                                              info=body['deliveryInfo'])
                return JsonResponse({'status': 'success',
                                     'redirect_url': normalize_url(settings.RECEIPT_URL + f'{receipt_id}/')},
                                    status=200)
            else:
                return JsonResponse({'status': 'failed',
                                     'message': 'not enough amount on credit card'}, status=400)
        else:
            return JsonResponse({'status': 'failed',
                                 'message': 'credit card not valid'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def user_update(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        form = EditableUserInfo(body)
        if form.is_valid():
            # if form.cleaned_data['email'] != '':
            request.user.profile.email = form.cleaned_data['email']
            # if form.cleaned_data['deliveryAddress'] != '':
            request.user.profile.address = form.cleaned_data['deliveryAddress']
            # if form.cleaned_data['creditCard'] != '':
            request.user.profile.credit_card = processing.get_credit_card(form.cleaned_data['creditCard'])
            request.user.save();
            return JsonResponse({'status': 'success'}, status=201)
        else:
            return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def get_receipt(request, id):
    receipt = processing.get_receipt(id)
    if receipt is not None:
        return render(request, 'receipt.html', {'receipt': receipt})
    return Http404()
