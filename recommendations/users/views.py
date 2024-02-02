from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView

from users.forms import AddressForm, LoginForm, SignupForm
from users.models import Profile


class IndexView(TemplateView):
    template_name = 'users/index.html'
    description = ('Миссия и цели: организация «Еще не бабушка» выроса из одноименного волонтерского движения, '
                   'главной задачей которого было улучшение жизни пожилых людей в интернатах и уменьшение '
                   'того эмоционального вакуума, в котором они оказываются после попадания в интернат. '
                   'Мы прошли большой путь от поездок в несколько интернатов до участия в выстраивании'
                   ' системы помощи пожилым людям и инвалидам на государственном уровне.  '
                   'И мы всегда стояли и стоим на том, что система должна быть для человека, а не человек для системы.'
                   'Миссия организации: Мы стараемся объединить ресурсы общества и государства для улучшения качества'
                   ' жизни пожилых людей. Наша стратегическая цель: Выстроить в стране систему помощи, '
                   'которая будет доступна каждому пожилому человеку, нуждающемуся в помощи.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = self.description
        return context


class UserSignUpView(FormView):
    template_name = "users/login.html"
    form_class = SignupForm(prefix='signup')
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:index')
    extra_context = {'message': 'Заполните данные о себе, пожалуйста:'}

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        profile = authenticate(username=username, password=password)
        if profile is not None:
            login(self.request, profile)
            messages.success(self.request, 'Вы успешно зарегистрировались.')
        return super(UserSignUpView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы уже вошли в систему.')
            return redirect(reverse('users:index'))
        else:
            return super(UserSignUpView, self).get(request)


def signup(request):
    if not request.user.is_authenticated:
        message = 'Заполните данные о себе, пожалуйста'
        signup_form = SignupForm(request.POST or None, prefix='signup')
        address_form = AddressForm(request.POST or None, prefix='address')
        if signup_form.is_valid() and address_form.is_valid():
            data = signup_form.cleaned_data
            address = address_form.cleaned_data
            Profile.objects.create_user(
                username=data['username'],
                password=data['password'],
                birth_date=data['birth_date'],
                address=f"город Москва, {address['street_name']}",
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
            {'form': signup_form, 'address_form': address_form, 'message': message}
        )
    else:
        return redirect(reverse('users:index'))


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:index')
    extra_context = {'message': 'Введите ваше имя и пароль:'}

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        profile = authenticate(username=username, password=password)
        if profile is not None:
            login(self.request, profile)
            messages.success(self.request, 'Вы успешно вошли в систему.')
        return super(UserLoginView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы уже вошли в систему.')
            return redirect(reverse('users:index'))
        else:
            return super(UserLoginView, self).get(request)


class UserLogOutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:index'))

# def user_login(request):
#     if not request.user.is_authenticated:
#         message = 'Введите ваше имя и пароль:'
#         form = LoginForm(request.POST or None)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             profile = authenticate(username=username, password=password)
#             if profile is not None:
#                 login(request, profile)
#                 messages.success(request, 'Вы успешно вошли в систему.')
#                 return redirect(reverse('users:index'))
#         return render(
#             request,
#             'users/login.html',
#             {'form': form, 'user': request.user, 'message': message}
#         )
#     else:
#         return redirect(reverse('users:index'))
