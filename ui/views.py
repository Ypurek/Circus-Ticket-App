from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
import logging

# logger = logging.getLogger(__name__)
LOGIN_URL = '/login'


def index(request):
    return HttpResponse('hello')


def login(request):
    if request.method == 'POST':
        if request.POST['username'] == 'aaa':
            return JsonResponse({'foo': 'bar'})
        else:
            return redirect('/ui/booking/')
    elif request.method == 'GET':
        return render(request, 'login.html')


def main(request):
    return render(request, 'booking.html')


@login_required(login_url=LOGIN_URL)
def search_tickets_form(request):
    pass


@login_required(login_url=LOGIN_URL)
def user_info(request):
    pass
