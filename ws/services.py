from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SearchTicketsForm, AddPerformanceForm, check_if_array, check_if_array_contains_str
from core import processing
from .helper import *
import datetime, json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def performances(request):
    # TODO test OPTION method
    if request.method == 'GET':
        return get_performances(request)
    elif request.method == 'POST':
        return add_performance(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def get_performances(request):
    form = SearchTicketsForm(request.GET)
    if form.is_valid():
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_from']
        time_from = form.cleaned_data['time_from']
        time_to = form.cleaned_data['time_to']
        price_from = form.cleaned_data['price_from']
        price_to = form.cleaned_data['price_to']
        description = form.cleaned_data['description']

        date_from = date_from or datetime.date.today()
        date_to = date_to or datetime.date.max
        time_from = time_from or datetime.time(hour=10)
        time_to = time_to or datetime.time(hour=22)
        price_from = price_from if price_from is not None else 0
        price_to = price_to or 9999999
        description = description if description is not None else ''

        perf_list = processing.get_performances(date_from,
                                                date_to,
                                                time_from,
                                                time_to,
                                                price_from,
                                                price_to,
                                                description)

        response = {'performanceList': []}
        for performance in perf_list:
            response['performanceList'].append(performance_to_json(performance))

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
            return JsonResponse(performance_to_json(p), status=409)
        performance = processing.add_performance(date=form.cleaned_data['date'],
                                                 time=form.cleaned_data['time'],
                                                 price=form.cleaned_data['price'],
                                                 description=form.cleaned_data['description'],
                                                 features=form.cleaned_data['features'])
        processing.add_tickets(performance, form.cleaned_data['ticketsNumber'])

        return JsonResponse(performance_to_json(performance), status=201)
    else:
        return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
