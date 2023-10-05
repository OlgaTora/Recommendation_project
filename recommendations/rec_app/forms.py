import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


# class ProfileCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Profile
#         fields = ('username', 'password', 'birth_date', 'address', 'gender')


class SignupForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    # confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    birth_date = forms.DateField(initial=datetime.date.today,
                                 widget=forms.DateInput(attrs={'class': 'date'}))
    address = forms.CharField(max_length=255)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')])

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Username cant contains spaces')
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is exist')
        return username

    # def clean_password(self):
    #     cleaned_data = self.cleaned_data
    #     password = self.cleaned_data('password')
    #     confirm_password = cleaned_data.get('confirm_password')
    #
    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords must be same")
    #     else:
    #         return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = Profile.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password!")
            return super(LoginForm, self).clean()
        except Profile.DoesNotExist:
            raise forms.ValidationError('Incorrect username')

