from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SearchTicketsForm
from core import processing
import datetime


def get_tickets(request):
    if request.method == 'GET':
        form = SearchTicketsForm(request.GET)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_from']
            time_from = form.cleaned_data['time_from']
            time_to = form.cleaned_data['time_to']
            price_from = form.cleaned_data['price_from']
            price_to = form.cleaned_data['price_to']
            description = form.cleaned_data['description']

            date_from = date_from if date_from is not None else datetime.datetime.date().today()
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