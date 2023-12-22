from django.db import models

from catalog.models import ActivityTypes
from users.models import Profile


class Question(models.Model):
    question_text = models.CharField(max_length=255, default='')
    questions = models.Manager()

    # def get_choices(self):
    #     return [(choice.votes, choice.choice_text) for choice in Choice.choices.filter(question=self)]

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    choices = models.Manager()

    def __str__(self):
        return self.choice_text


class TestResultDescription(models.Model):
    activity_type = models.ForeignKey(ActivityTypes, on_delete=models.CASCADE)
    description = models.TextField()
    descriptions = models.Manager()

    def __str__(self):
        return self.description


class ResultOfTest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    results = models.Manager()

    @staticmethod
    def get_results(user):
        results = ResultOfTest.results.filter(user=user)
        resume = 0
        for result in results:
            resume += result.answer.votes
        return resume
