from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.conf import settings

import logging
import requests


class AuthenticationBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        api_req = get_user_from_api(email, password)
        if api_req is None:
            return None
        elif not api_req:
            return False

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = User(username=email)
            user.is_staff = True
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def get_user_from_api(username, password):
    payload = {
        'email': username,
        'password': password
    }

    req = requests.post(url=settings.GET_USER_ENDPOINT, data=payload)
    response = req.json()

    # check if user is authenticated
    if req:
        # check if it has notification
        if response["notification"]:
            return True
        else:
            return None
    else:
        return False


