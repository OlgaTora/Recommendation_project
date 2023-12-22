import os
import csv
import django

from django.core.management.base import BaseCommand

from catalog.models import ActivityTypes
from rec_app.models import Question, Choice, TestResultDescription

N_QUEST = 10  # 22
N_ANS = 5  # 132


class Command(BaseCommand):
    help = "Generate database from file."

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()

        with open('files/list_questions.csv', 'r', encoding='utf-8') as questions:
            question_list = []
            file_reader = csv.reader(questions, delimiter=';')
            for row in file_reader:
                question_list.append(row)
        print(question_list)

        with open('files/list_answers.csv', 'r', encoding='utf_8') as choices:
            choice_list = []
            file_reader = csv.reader(choices, delimiter=';')
            for row in file_reader:
                choice_list.append(row)
        print(choice_list)

        for i in range(1, N_QUEST + 1):
            Question.questions.create(
                question_text=question_list[i][0],
            )
            print(f'Question {i} added')

        for j in range(1, N_ANS + 1):
            Choice.choices.create(
                choice_text=choice_list[j][0],
                votes=choice_list[j][1],
            )
            print(f'Choice {j} added')

        with open('files/test_result.csv', 'r', encoding='utf-8') as results:
            file_reader = csv.reader(results, delimiter=';')
            for row in file_reader:
                TestResultDescription.descriptions.create(
                    description=row[1],
                    activity_type=ActivityTypes.types.filter(activity_type=row[0]).first(),
                )
