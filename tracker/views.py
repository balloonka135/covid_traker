from django.shortcuts import render
from django.contrib.auth import logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import requests

from .models import UserProfile
from .forms import UserCreateForm


def index(request):
    # landing related data
    r = requests.get(url=settings.STAT_API_ENDPOINT)
    data = r.json()

    inf = data['infected']
    infected = split_integer(inf)

    dec = data['deceased']
    deceased = split_integer(dec)

    rec = data['recovered']
    recovered = split_integer(rec)

    context = {
        'infected': infected,
        'deceased': deceased,
        'recovered': recovered
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        occupation = request.POST.get('occupation')
        status = request.POST.get('status')

        payload = {
            'email': email,
            'password': password,
            'name': name,
            'occupation': occupation,
            'status': status,
        }

        req = requests.post(url=settings.CREATE_USER_ENDPOINT, data=payload)

    return render(request, 'tracker/index.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            return HttpResponseRedirect('/')
        else:
            print("The login had failed. Check the correctness of the username/password.")
            return HttpResponse("Invalid login credentials.")
    else:
        return render(request, 'tracker/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_update_status(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        updated_status = request.POST.get('status')

        payload = {
            'email': email,
            'status': updated_status
        }

        req = requests.put(url=settings.UPDATE_USER_STATUS, data=payload)

        if req:
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Error occured while updating status.")
    else:
        return render(request, 'tracker/update_status.html', {})


def split_integer(number):
    return int(number) / 1000








