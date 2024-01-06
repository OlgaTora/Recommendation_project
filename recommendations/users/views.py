from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import AddressForm, LoginForm, SignupForm
from users.models import Profile


def index(request):
    description = ('Миссия и цели: организация «Еще не бабушка» выроса из одноименного волонтерского движения, '
                   'главной задачей которого было улучшение жизни пожилых людей в интернатах и уменьшение '
                   'того эмоционального вакуума, в котором они оказываются после попадания в интернат. '
                   'Мы прошли большой путь от поездок в несколько интернатов до участия в выстраивании'
                   ' системы помощи пожилым людям и инвалидам на государственном уровне.  '
                   'И мы всегда стояли и стоим на том, что система должна быть для человека, а не человек для системы.'
                   'Миссия организации: Мы стараемся объединить ресурсы общества и государства для улучшения качества'
                   ' жизни пожилых людей. Наша стратегическая цель: Выстроить в стране систему помощи, '
                   'которая будет доступна каждому пожилому человеку, нуждающемуся в помощи.')
    return render(request, 'users/index.html', {'description': description})


def signup(request):
    if not request.user.is_authenticated:
        message = 'Заполните данные о себе, пожалуйста'
        address_form = AddressForm(request.POST or None)
        signup_form = SignupForm(request.POST or None)

        if address_form.is_valid() and signup_form.is_valid():
            data = signup_form.cleaned_data
            address = address_form.cleaned_data
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
                messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect(reverse('users:index'))
        return render(
            request,
            'users/login.html',
            {'signup_form': signup_form, 'address_form': address_form, 'message': message}
        )
    else:
        return redirect(reverse('users:index'))


def user_login(request):
    if not request.user.is_authenticated:
        message = 'Введите ваше имя и пароль'
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile = authenticate(username=username, password=password)
            if profile is not None:
                login(request, profile)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect(reverse('users:index'))
        return render(
            request,
            'users/login.html',
            {'form': form, 'user': request.user, 'message': message}
        )
    else:
        return redirect(reverse('users:index'))


@login_required(redirect_field_name='/')
def user_logout(request):
    if request.user is not None:
        logout(request)
    return redirect(reverse('users:index'))

#
# @login_required(redirect_field_name='/')
# def district_choice(request):
#     message = ''
#     form = DistrictForm(request.POST or None)
#     if form.is_valid():
#         district = form.cleaned_data['district']
#         return redirect(reverse('rec_app:recommendations'))
#     return render(
#         request,
#         'users/login.html',
#         {'form': form, 'user': request.user, 'message': message}
#     )