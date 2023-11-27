import os
import csv
import django

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from rec_app.models import Profile, Question, Choice

N_QUEST = 10  # 22
N_ANS = 5  # 132


class Command(BaseCommand):
    help = "Generate database from file."

    def handle(self, *args, **kwargs):

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()

        # with open('files/users.csv', 'r', encoding='utf-8') as users:
        #     users_list = []
        #     file_reader = csv.reader(users, delimiter=',')
        #     for row in file_reader:
        #         users_list.append(row)

        # for i in range(1, 51):  # len(users_list)+1):
        #     Profile.objects.create(
        #         username=users_list[i][0],
        #         password=make_password(users_list[i][0]),
        #         date_joined=users_list[i][1],
        #         gender=users_list[i][2],
        #         birth_date=users_list[i][3],
        #         address=users_list[i][4],
        #     )

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

    # n = 1
    # for i in range(1, N_QUEST + 1):
    #     for j in range(n, int(N_ANS / N_QUEST) + n):
    #         choice = Choice.choices.create(
    #             question=Question.questions.get(id=i),
    #             choice_text=choice_list[j][0],
    #             votes=choice_list[j][1],
    #         )
    #         print("Choice {} added".format(j))
    #     n += 6
    #     print("Question {} close".format(i))
