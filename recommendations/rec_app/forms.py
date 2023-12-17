from datetime import timedelta, date
from django import forms
from django.utils import timezone

from address_book.models import StreetsBook
from .models import Profile, Question, Choice, ResultOfTest


class SignupForm(forms.Form):
    username = forms.CharField(max_length=12, label='Имя')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='Пароль')
    # confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    birth_date = forms.DateField(initial=date.today,
                                 widget=forms.DateInput(attrs={'class': 'date'}), label='Дата рождения')
    address = forms.ModelChoiceField(queryset=StreetsBook.streets.all(), required=False, label='Адрес')

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


class AnswerForm(forms.Form):
    def __init__(self, *args, page_num, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page_num
        self.user = user
        choices = []
        question_pk = self.page
        self.question = Question.questions.get(pk=question_pk)
        for choice in Choice.choices.all():
            choices.append((choice.votes, choice.choice_text))

        self.fields['choice'] = forms.ChoiceField(
            label=self.question.question_text,
            required=True,
            choices=choices,
            widget=forms.RadioSelect)

    def clean(self):
        if ResultOfTest.results.filter(user=self.user, question=self.question).exists():
            raise forms.ValidationError(f'Вы уже отвечали на вопросы теста.')
        else:
            return super(AnswerForm, self).clean()

    def save(self):
        choice = int(self.cleaned_data['choice'])
        answer = Choice.choices.get(votes=choice)
        result = ResultOfTest(answer=answer, user=self.user, question=self.question)
        result.save()

