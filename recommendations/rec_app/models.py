from django.db import models

from catalog.models import ActivityTypes
from users.models import Profile


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.choice_text


class TestResultDescription(models.Model):
    activity_type = models.ForeignKey(ActivityTypes, on_delete=models.CASCADE)
    description = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.description


class ResultOfTest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    objects = models.Manager()

    @staticmethod
    def get_results(user):
        results = ResultOfTest.objects.filter(user=user)
        resume = 0
        for result in results:
            resume += result.answer.votes
        return resume


class VotesGroups(models.Model):
    result_group = models.ForeignKey(TestResultDescription, on_delete=models.CASCADE)
    votes = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return f'{self.votes}'
