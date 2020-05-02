from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

from .models import UserProfile


# login form
class UserSignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


# additional user form
class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = (
            'profile_url', 'profile_pic'
        )


# user personal form for sharing data
class UserShareDataForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = (
            'occupation', 'infection_status'
        )
