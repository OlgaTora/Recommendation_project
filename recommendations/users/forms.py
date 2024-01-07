from datetime import timedelta, date
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from address_book.models import StreetsBook
from .models import Profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = StreetsBook
        exclude = ('index',)


class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'password', 'birth_date', 'gender']

    username = forms.CharField(max_length=12, label='Имя')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='Пароль')
    #confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    birth_date = forms.DateField(initial=date.today,
                                 widget=forms.DateInput(attrs={'class': 'date'}), label='Дата рождения')
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')],
                               label='Пол')

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя не может содержать пробелы.')
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError('Такое имя уже существует.')
        return username

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        now = timezone.now().date()
        if birth_date > (now - timedelta(days=30)):
            raise forms.ValidationError('Неверная дата рождения.')
        if (now.year - birth_date.year) > 120:
            raise forms.ValidationError('Неверная дата рождения.')
        return birth_date

    # def clean(self):
    #     data = self.cleaned_data
    #     password = data.get('password')
    #     validate_password(password)
    #     if password != data.get('confirm_password'):
    #         raise forms.ValidationError('Пароли должны быть одинаковыми')
    #     else:
    #         return data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = Profile.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError("Неправильно введен пароль.")
            return super(LoginForm, self).clean()
        except Profile.DoesNotExist:
            raise forms.ValidationError('Неправильно введено имя.')


"""

class SignupForm(forms.Form):
    username = forms.CharField(max_length=12, label='Имя')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='Пароль')
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    birth_date = forms.DateField(initial=date.today,
                                 widget=forms.DateInput(attrs={'class': 'date'}), label='Дата рождения')
    # admin_district = forms.ModelChoiceField(queryset=StreetsBook.streets_book.all().values('admin_district').distinct())
    # district = forms.ModelChoiceField(queryset=StreetsBook.streets_book.all().values('district').distinct(), label='Адрес')
    # address = forms.ModelChoiceField(queryset=StreetsBook.streets_book.all(), required=False, label='Адрес')
    # types = forms.ModelChoiceField(queryset=StreetsBook.streets_book.all(), required=False, label='Type')

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')],
                               label='Пол')

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя не может содержать пробелы.')
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError('Такое имя уже существует.')
        return username

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        now = timezone.now().date()
        if birth_date > (now - timedelta(days=30)):
            raise forms.ValidationError('Неверная дата рождения.')
        if (now.year - birth_date.year) > 120:
            raise forms.ValidationError('Неверная дата рождения.')
        return birth_date

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        validate_password(password)
        if password != data.get('confirm_password'):
            raise forms.ValidationError('Пароли должны быть одинаковыми')
        else:
            return data
"""