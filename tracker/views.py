from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import requests
import logging

from .models import UserProfile
from .forms import UserCreateForm

from .logging_manager import LoggingManager, upload_file_s3


logger = LoggingManager()


def index(request):
    logging.info('Requesting covid statistics data.')
    r = requests.get(url=settings.STAT_API_ENDPOINT)
    data = r.json()

    inf = data.get('infected')
    infected = split_integer(inf)

    dec = data.get('deceased')
    deceased = split_integer(dec)

    rec = data.get('hospitalised')
    recovered = split_integer(rec)

    auth = bool(request.GET.get('auth', False))
    notification = bool(request.GET.get('msg', False))

    context = {
        'infected': infected,
        'deceased': deceased,
        'recovered': recovered,
        'is_authenticated': auth,
        'has_notification': notification
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

        logging.info('Sending API request to create user.')

        try:
            req = requests.post(url=settings.CREATE_USER_ENDPOINT, data=payload)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return HttpResponse("Error occured while creating a user.")

    logging.info('Rendering index page.')
    upload_file_s3(logger.filename, "webapplogger")

    return render(request, 'tracker/index.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        logging.info('Authenticating user profile.')
        user = authenticate(request, username=username, password=password)

        if user:
            logging.info('User is authenticated and has a notification.')
            upload_file_s3(logger.filename, "webapplogger")

            return redirect('{}?auth=True&msg=True'.format(reverse('index')))
        elif user is None:
            logging.info('User is authenticated and does not have any notifications.')
            upload_file_s3(logger.filename, "webapplogger")

            return redirect('{}?auth=True&msg=False'.format(reverse('index')))
        else:
            logging.error("The login had failed. Check the correctness of the username/password.")
            upload_file_s3(logger.filename, "webapplogger")

            return HttpResponse("Invalid login credentials.")
    else:
        return render(request, 'tracker/login.html')


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

        logging.info('Sending API request to update user status.')
        upload_file_s3(logger.filename, "webapplogger")

        try:
            req = requests.put(url=settings.UPDATE_USER_STATUS, data=payload)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            upload_file_s3(logger.filename, "webapplogger")

            return HttpResponse("Error occured while updating status.")
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'tracker/update_status.html', {})


def run_simulation(request):
    if request.method == 'POST':
        pop_size = request.POST.get('pop_size')
        initial_infected = request.POST.get('initial_infected')
        initial_exposed = request.POST.get('initial_exposed')
        nr_hospitals = request.POST.get('nr_hospitals')
        governmental_policy = request.POST.get('governmental_policy')
        nbr_days = request.POST.get('nbr_days')
        incubation_period = request.POST.get('incubation_period')
        recovery_period = request.POST.get('recovery_period')
        mortality_rates = request.POST.get('mortality_rates')


        payload = {
            'pop_size': pop_size,
            'initial_infected': initial_infected,
            'initial_exposed': initial_exposed,
            'nr_hospitals': nr_hospitals,
            'governmental_policy': governmental_policy,
            'nbr_days': nbr_days,
            'incubation_period': incubation_period,
            'recovery_period': recovery_period,
            'mortality_rates': mortality_rates
        }

        logging.info('Sending API request to run the simulation.')
        upload_file_s3(logger.filename, "webapplogger")

        try:
            req = requests.post(url=settings.SIM_API_ENDPOINT, data=payload)
            timestamp_response = req.json()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            upload_file_s3(logger.filename, "webapplogger")

            return HttpResponse("Error occured while starting the simulation.")
        else:
            redirect_url = settings.KIBANA_DASHBOARD.format(timestamp=timestamp_response)
            return HttpResponseRedirect(redirect_url)
    else:
        return render(request, 'tracker/simulation.html')


def split_integer(number):
    if number:
        return ("{:,}".format(number))
    return None








