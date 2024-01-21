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

        with open('files/users.csv', 'r', encoding='utf-8') as users:
            file_reader = csv.reader(users, delimiter=',')
            next(file_reader)
            for row in file_reader:
                Profile.objects.create(
                    username=row[0],
                    password=make_password(row[0]),
                    date_joined=row[1],
                    gender=row[2],
                    birth_date=row[3],
                    address=row[4],
                )

