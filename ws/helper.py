import datetime
import json

from django.http import JsonResponse

from core import processing, operations
from .forms import AddPerformanceForm, GetTicketsForm
from core.forms import GetPerformanceForm


def get_performances(request):
    form = GetPerformanceForm(request.GET)
    if form.is_valid():
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        time_from = form.cleaned_data['time_from']
        time_to = form.cleaned_data['time_to']
        price_from = form.cleaned_data['price_from']
        price_to = form.cleaned_data['price_to']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']

        date_from = date_from or datetime.date.today()
        date_to = date_to or datetime.date.max
        time_from = time_from or datetime.time(hour=10)
        time_to = time_to or datetime.time(hour=22)
        price_from = price_from if price_from is not None else 0
        price_to = price_to or 9999999

        perf_list = processing.get_performances(date_from, date_to,
                                                time_from, time_to,
                                                price_from, price_to,
                                                name, description)

        response = {'performanceList': []}
        for performance in perf_list:
            response['performanceList'].append(operations.performance_to_json(performance))

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)


def add_performance(request):
    try:
        form = AddPerformanceForm(json.loads(request.body))
        val = form.is_valid()
    except:
        return JsonResponse({'status': 'failed', 'message': 'invalid json provided'}, status=400)
    if val:
        p = processing.get_performance(date=form.cleaned_data['date'], time=form.cleaned_data['time'])
        if p is not None:
            return JsonResponse(operations.performance_to_json(p), status=409)
        performance = processing.add_performance(date=form.cleaned_data['date'],
                                                 time=form.cleaned_data['time'],
                                                 price=form.cleaned_data['price'],
                                                 name=form.cleaned_data['name'],
                                                 description=form.cleaned_data['description'],
                                                 features=form.cleaned_data['features'])
        tickets = form.cleaned_data['ticketsNumber']
        if tickets is not None:
            processing.add_tickets(performance, tickets)

        return JsonResponse(operations.performance_to_json(performance), status=201)
    else:
        return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)


def get_performance(id):
    try:
        p = processing.get_performance_by_id(id)
    except:
        return JsonResponse({'status': 'failed', 'message': 'id format invalid'}, status=400)
    if p is None:
        return JsonResponse({'status': 'failed', 'message': 'performance not found'}, status=404)
    return JsonResponse(operations.performance_to_json(p), status=200)


def update_performance(request, id):
    try:
        form = AddPerformanceForm(json.loads(request.body))
        val = form.is_valid()
    except:
        return JsonResponse({'status': 'failed', 'message': 'invalid json provided'}, status=400)
    if val:
        p = processing.update_performance(id=id,
                                          date=form.cleaned_data['date'],
                                          time=form.cleaned_data['time'],
                                          price=form.cleaned_data['price'],
                                          name=form.cleaned_data['name'],
                                          description=form.cleaned_data['description'],
                                          features=form.cleaned_data['features'])
        if p is not None:
            return JsonResponse(operations.performance_to_json(p), status=202)
        else:
            return JsonResponse({'status': 'failed', 'message': 'performance not found'}, status=404)
    else:
        return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)


def get_tickets(request):
    form = GetTicketsForm(request.GET)
    if form.is_valid():
        result = {'totalCount': 0,
                  'tickets': []}
        tickets = processing.get_tickets()
        result['totalCount'] = tickets.count()
        page = form.cleaned_data['page']
        size = form.cleaned_data['size']
        performance_id = form.cleaned_data['performanceID']
        status = form.cleaned_data['status']
        print(performance_id, type(performance_id))
        print(status, type(status))
        if performance_id is not None:
            tickets = tickets.filter(performance__id=performance_id)
            result['filteredCount'] = tickets.count()
        if len(status) != 0:
            tickets = tickets.filter(status=status)
            result['filteredCount'] = tickets.count()

        ticket_range = tickets[(page - 1) * size:page * size]
        for t in ticket_range:
            result['tickets'].append(operations.ticket_to_json(t))
        return JsonResponse(result, status=200)
    else:
        return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)


def get_ticket(id):
    t = processing.get_ticket(id)
    if t is None:
        return JsonResponse({'status': 'failed', 'message': 'ticket not found'}, status=404)
    else:
        return JsonResponse({'id': t.id,
                             'performance':
                                 {'id': t.performance.id,
                                  'name': t.performance.name},
                             'status': t.status}, status=200)


def delete_ticket(id):
    t = processing.get_ticket(id)
    if t is None:
        return JsonResponse({'status': 'failed', 'message': 'ticket not found'}, status=404)
    else:
        if processing.delete_ticket(id):
            return JsonResponse({'result': 'deleted'}, status=200)
        else:
            return JsonResponse({'result': 'failed to delete'}, status=500)


def get_lucky():
    return JsonResponse({'maxTicketToBook': processing.get_app_property('max_book_ticket'),
                         'buyCounter': processing.get_app_property('user_buy_counter'),
                         'buyCounterLimit': processing.get_app_property('user_buy_counter_limit'),
                         'buyCounterDiscount': processing.get_app_property('user_buy_counter_discount'),
                         'emailDiscount': processing.get_app_property('user_logged_in_discount'),
                         'snackPrice': processing.get_app_property('snack_price'),
                         'bookingTimeout': processing.get_app_property('booking_timeout')}, status=417)