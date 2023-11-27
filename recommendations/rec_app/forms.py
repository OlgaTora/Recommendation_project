import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import BaseFormSet

from . import models
from .models import Profile, Question, Choice


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


class AnswerForm(forms.Form):

    def __init__(self, *args, page_num, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        question_pk = page_num
        question = Question.questions.filter(pk=question_pk).first()
        for choice in Choice.choices.all():
            choices.append((choice.votes, choice.choice_text))
        # for choice in question.choice_set.all():
            # choices.append((choice.votes, choice.choice_text))
        # self.fields['choice'] = forms.ChoiceField(label=question.question_text, required=True,
        #                                         choices=choices, widget=forms.RadioSelect)
        self.fields['choice'] = forms.ChoiceField(
            label=question.question_text,
            required=True,
            choices=choices,
            widget=forms.RadioSelect)
