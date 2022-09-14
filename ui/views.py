from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import EditableUserInfo, SimpleTicketSearchForm
from core import processing, operations
from . import settings
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
import json


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
               'display_search_results': False,
               # BUG some hardcoded UI bug
               'keyword_bug': True}

    if request.method == 'GET':
        form = SimpleTicketSearchForm()
        form.time_interval = '420,1380'
        form.price_interval = '0,1000'

    if request.method == 'POST':
        form = SimpleTicketSearchForm(request.POST)
        if form.is_valid():
            context['form'] = form
            context['display_search_results'] = True
            time = form.cleaned_data['time_interval'].split(',')
            price = form.cleaned_data['price_interval'].split(',')
            time_interval = int(time[0]), int(time[1])
            price_interval = int(price[0]), int(price[1])
            perf_list = processing.get_performance_simple(date_from=form.cleaned_data['date_from'],
                                                          date_to=form.cleaned_data['date_to'],
                                                          time_interval=time_interval,
                                                          price_interval=price_interval,
                                                          keyword=form.cleaned_data['keyword'])
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
def buy_info(request):
    tickets = request.user.booked_tickets.all()
    if len(tickets) == 0:
        return redirect(normalize_url(settings.BOOKING_URL))


    context = {'user': request.user,
               'tickets': tickets,
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
               'booked_tickets_list': request.user.booked_tickets.filter(),
               'bought_tickets_list': request.user.bought_tickets.filter(),
               # BUG some hardcoded UI
               'user_info_bug': True}

    return render(request, 'user_info.html', context)


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def update_price(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        result = operations.update_invoice(user=request.user, updates_list=body)
        if result.get('status') is not None:
            return JsonResponse(result, status=400)
        return JsonResponse(result, status=200)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def process_payment(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        form = EditableUserInfo(body)
        if not form.is_valid():
            return JsonResponse({'status': 'failed',
                                 'message': form.errors}, status=400)

        # TODO BUG?
        if request.user.booked_tickets == 0:
            return JsonResponse({'status': 'failed',
                                 'message': 'too late - tickets not booked. Please refresh page'}, status=400)


        if len(body['coupon']) > 0 and not processing.check_discount_code(body['coupon']):
            return JsonResponse({'status': 'failed',
                                 'message': {'coupon': 'discount coupon not found'}}, status=400)

        payment_info = operations.update_invoice(user=request.user, updates_list=body)
        cc = processing.check_credit_card(card_number=body['creditCard'],
                                          amount=payment_info['finalPrice'])

        if cc['is_valid']:
            # BUG
            if cc['is_enough']:
                receipt_id = operations.debit(user=request.user,
                                              price=payment_info['totalPrice'],
                                              discount=payment_info['totalDiscount'],
                                              credit_card=processing.get_credit_card(body['creditCard']),
                                              tickets_list=request.user.booked_tickets.all(),
                                              discount_code=body['coupon'],
                                              info=body['deliveryAddress'])
                return JsonResponse({'status': 'success',
                                     'redirect_url': normalize_url(settings.RECEIPT_URL + f'{receipt_id}/')},
                                    status=200)
            else:
                return JsonResponse({'status': 'failed',
                                     'message': {'creditCard': 'not enough amount on credit card'}}, status=400)
        else:
            return JsonResponse({'status': 'failed',
                                 'message': {'creditCard': 'credit card not valid'}}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def user_update(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        form = EditableUserInfo(body)
        if form.is_valid():
            request.user.profile.email = form.cleaned_data['email']
            request.user.profile.address = form.cleaned_data['deliveryAddress']
            addr = form.cleaned_data['deliveryAddress']
            if addr.find('>') >= 0 or addr.find('<') >= 0:
                return JsonResponse(
                    {'status': 'failed', 'message': 'no html tags allowed. don\'t care about requirements ;)'},
                    status=400)

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
        if receipt.user != request.user:
            return redirect('/403')
        return render(request, 'receipt.html', {'receipt': receipt})
    return redirect('/404')


@login_required(login_url=normalize_url(settings.LOGIN_URL))
def release_ticket(request, id):
    ticket = processing.get_ticket(id)
    if ticket is not None:
        if ticket.status == 'booked':
            if ticket.booked_by == request.user:
                processing.release_booked_ticket(ticket, f'ticket was manually released by {request.user}')
                return JsonResponse({'message': 'success'}, status=200)
            else:
                return JsonResponse({'message': 'unauthorized'}, status=403)
        else:
            return JsonResponse({'message': 'ticket not booked'}, status=400)
    else:
        return JsonResponse({'message': 'ticket does not exist'}, status=400)