from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SearchTicketsForm, AddPerformanceForm, check_if_array, check_if_array_contains_str
from core import processing
import datetime
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
    try:
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_from']
            time_from = form.cleaned_data['time_from']
            time_to = form.cleaned_data['time_to']
            price_from = form.cleaned_data['price_from']
            price_to = form.cleaned_data['price_to']
            description = form.cleaned_data['description']

            date_from = date_from if date_from is not None else datetime.date.today()
            date_to = date_to if date_to is not None else datetime.date(datetime.MAXYEAR, 12, 31)
            time_from = time_from if time_from is not None else datetime.time(hour=10)
            time_to = time_to if time_to is not None else datetime.time(hour=22)
            price_from = price_from if price_from is not None else 0
            price_to = price_to if price_to is not None else 9999999
            description = description if description is not None else ''

            perf_list = processing.get_performances(date_from,
                                                    date_to,
                                                    time_from,
                                                    time_to,
                                                    price_from,
                                                    price_to,
                                                    description)

            response = {'tickets': []}
            for performance in perf_list:
                feature_list = []
                for feature in performance.features.filter():
                    feature_list.append(feature.feature)
                response['tickets'].append({'id': performance.id,
                                            'date': performance.date,
                                            'time': performance.time,
                                            'description': performance.description,
                                            'price': performance.price,
                                            'features': feature_list,
                                            'ticketsNumber': performance.tickets.count()})

            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
    except Exception:
        return JsonResponse({'status': 'failed', 'message': 'bad request data'}, status=400)


def add_performance(request):
    form = AddPerformanceForm(request.POST)
    request.POST['features']
    try:
        if form.is_valid():
            performance = processing.add_performance(date=form.cleaned_data['date'],
                                                     time=form.cleaned_data['time'],
                                                     price=form.cleaned_data['price'],
                                                     description=form.cleaned_data['description'],
                                                     features=form.cleaned_data['features'])
            processing.add_tickets(performance, form.cleaned_data['ticketsNumber'])
            feature_list = []
            for feature in performance.features.filter():
                feature_list.append(feature.feature)
            return JsonResponse({'id': performance.id,
                                 'date': performance.date,
                                 'time': performance.time,
                                 'description': performance.description,
                                 'price': performance.price,
                                 'features': feature_list,
                                 'ticketsNumber': performance.tickets.count()}, status=201)
        else:
            return JsonResponse({'status': 'failed', 'message': form.errors}, status=400)
    except Exception:
        return JsonResponse({'status': 'failed', 'message': 'bad request data'}, status=400)
