import os
import csv
import django

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from recommendations.rec_app.models import Profile


class Command(BaseCommand):
    help = "Generate database from file."

    def handle(self, *args, **kwargs):

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()

        with open('files/users.csv', 'r', encoding='utf-8') as users:
            users_list = []
            file_reader = csv.reader(users, delimiter=',')
            for row in file_reader:
                users_list.append(row)

        print("done")
        for i in range(1, 51):  # len(users_list)+1):
            Profile.objects.create(
                username=users_list[i][0],
                password=make_password(users_list[i][0]),
                date_joined =users_list[i][1],
                gender=users_list[i][2],
                birth_date=users_list[i][3],
                address=users_list[i][4],
            )
