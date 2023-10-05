from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    class Gender(models.TextChoices):
        WOMAN = 'Женщина'
        MAN = 'Мужчина'

    date_joined = models.DateField(auto_now_add=True)
    birth_date = models.DateField()
    gender = models.CharField(choices=Gender.choices, max_length=7)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Имя: {Profile.username} пол: {self.gender}'


class Question(models.Model):
    question_text = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

