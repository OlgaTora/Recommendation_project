import os
import csv
import django

from django.core.management.base import BaseCommand

from catalog.models import ActivityTypes
from rec_app.models import Question, Choice, TestResultDescription, VotesGroups


class Command(BaseCommand):
    help = "Generate database from file."

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()

        with open('files/list_questions.csv', 'r', encoding='utf-8') as questions:
            file_reader = csv.reader(questions, delimiter=';')
            next(file_reader)
            for row in file_reader:
                Question.questions.create(
                            question_text=row[0],
                         )

        with open('files/list_answers.csv', 'r', encoding='utf_8') as choices:
            file_reader = csv.reader(choices, delimiter=';')
            next(file_reader)
            for row in file_reader:
                Choice.choices.create(
                             choice_text=row[0],
                             votes=row[1]
                )

        with open('files/test_result.csv', 'r', encoding='utf-8') as results:
            file_reader = csv.reader(results, delimiter=';')
            next(file_reader)
            for row in file_reader:
                TestResultDescription.descriptions.create(
                    activity_type=ActivityTypes.types.get(pk=row[0]),
                    description=row[1],
                )

        with open('files/votes_groups.csv', 'r', encoding='utf-8') as votes:
            file_reader = csv.reader(votes, delimiter=';')
            next(file_reader)
            for row in file_reader:
                VotesGroups.votes_groups.create(
                    votes=row[0],
                    result_group=TestResultDescription.descriptions.get(pk=row[1]),
                )
