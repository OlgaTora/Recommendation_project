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


