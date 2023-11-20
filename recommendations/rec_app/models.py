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
        return f'Имя: {self.username}'


class Question(models.Model):
    question_text = models.CharField(max_length=255, default='')

    def get_choices(self):
        return [(choice.votes, choice.choice_text) for choice in Choice.objects.filter(question=self)]

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class ResultOfTest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @staticmethod
    def get_results(user):
        results = ResultOfTest.objects.filter(user=user)
        resume = 0
        for result in results:
            resume += result.answer.votes
        return resume

