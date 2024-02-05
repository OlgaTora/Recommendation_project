import os
import csv
import django

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from users.models import Profile


class Command(BaseCommand):
    help = "Generate database from file."

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()
        with open('files/users_test.csv', 'r', encoding='utf-8') as users:
            profiles = []
            file_reader = csv.reader(users, delimiter=',')
            next(file_reader)
            for row in file_reader:
                profiles.append(row)

        for row in range(len(profiles)):
            Profile.objects.create(
                    username=profiles[row][0],
                    password=make_password(profiles[row][0]),
                    date_joined=profiles[row][1],
                    gender=profiles[row][2],
                    birth_date=profiles[row][3],
                    address=profiles[row][4],
                )
            print(row)
