from django.http import JsonResponse, HttpResponseNotAllowed
from .helper import *
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


@csrf_exempt
def performance(request, id):
    if request.method == 'GET':
        return get_performance(id)
    elif request.method == 'PUT':
        return update_performance(request, id)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT'])


@csrf_exempt
def tickets(request):
    if request.method == 'GET':
        return get_tickets(request)
    else:
        return HttpResponseNotAllowed(['GET'])