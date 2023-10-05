from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import http

from .forms import SignupForm, LoginForm
from .models import Profile


def index(request):
    return render(request, 'base.html')


def catalog(request):
    return render(request, 'catalog.html')


def search(request):
    return render(request, 'search.html')

def signup(request):
    message = 'Fill this form to sign up'
    if request.method == 'POST':
        form = SignupForm(request.POST, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Profile.objects.create_user(
                username=data['username'],
                password=data['password'],
                birth_date=data['birth_date'],
                address=data['address'],
                gender=data['gender'])

            user = authenticate(username=data['username'],
                                password=data['password'])
            if user is not None:
                login(request, user)
            return http.HttpResponseRedirect('')
    else:
        form = SignupForm()
    return render(
        request,
        'login.html',
        {'form': form, 'message': message}
    )


def user_login(request):
    message = 'Please, input username and password'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile = authenticate(username=username, password=password)
            if profile is not None:
                login(request, profile)
                # return HttpResponseRedirect('/')
                return render(request, 'base.html')
    else:
        form = LoginForm()
    return render(
        request,
        'login.html',
        {'form': form, 'user': request.user, 'message': message}
    )


def user_logout(request):
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect('/')
