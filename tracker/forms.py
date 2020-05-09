from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

from .models import UserProfile


# user personal form for sharing data
class UserShareDataForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = (
            'occupation', 'infection_status'
        )


# uniform form for user creation
class UserCreateForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=40)
    name = forms.CharField(max_length=100)
    occupation = forms.CharField(max_length=40)
    status = forms.CharField(max_length=20)
