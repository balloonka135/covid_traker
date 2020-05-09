from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.conf import settings


import requests


class AuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = request.GET.get('username')
        password = request.GET.get('password')

        if get_user_from_api(username, password) is None:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
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
        'username': username,
        'password': password
    }

    req = requests.get(url=settings.GET_USER_ENDPOINT, data=payload)
    response = req.json()

    if response[0]['message'] == 'SUCCESS':
        return response
    else:
        return None



