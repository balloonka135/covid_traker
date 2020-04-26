from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')


class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = (
            'profile_url', 'profile_pic', 'occupation', 'infection_status'
        )
