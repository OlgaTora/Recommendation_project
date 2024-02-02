from django.db import models
from django.db.models import Sum, Count

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
        counter_votes = len(ResultOfTest.objects.filter(user=user).annotate(count=Count("user")))
        # ответов меньше, чем вопросов
        if Question.objects.latest('pk').pk != counter_votes:
            return None
        result = ResultOfTest.objects.filter(user=user).values('answer__votes').aggregate(Sum('answer__votes'))
        return result['answer__votes__sum']


class VotesGroups(models.Model):
    result_group = models.ForeignKey(TestResultDescription, on_delete=models.CASCADE)
    votes = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return f'{self.votes}'
