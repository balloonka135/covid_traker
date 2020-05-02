from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserSignInForm, UserProfileForm, UserShareDataForm


def index(request):
    return render(request, 'tracker/index.html')


def user_register(request):
    user_registered = False

    if request.method == 'POST':
        user_form = UserSignInForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(request)
            user.set_password(user.password)
            user.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']
            user_profile.save()
            user_registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserSignInForm()
        user_profile_form = UserProfileForm()

    return render(request, 'tracker/registration.html', {
                        'user_form': user_form,
                        'profile_form': user_profile_form,
                        'registered': user_registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("The account is inactive.")
        else:
            print("The login had failed. Check the correctness of the username/password.")
            return HttpResponse("Invalid login credentials")
    else:
        return render(request, 'tracker/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_share_data(request):
    success = False
    if request.method == 'POST':
        user_form = UserShareDataForm(data=request.POST)
        if user_form.is_valid():
            user = UserProfile.objects.get(user=request.user)
            user_form = UserShareDataForm(data=request.POST, instance=user)
            user_form.save()
            success = True
        else:
            print(user_form.errors)
    else:
        user_form = UserShareDataForm()

    return render(request, 'tracker/user_profile_data.html', {
                        'user_form': user_form,
                        'success': success
    })

