from django.db import models


class ActivityTypes(models.Model):
    activity_type = models.CharField(max_length=255, unique=True)
    types = models.Manager()


class ActivityLevel1(models.Model):
    activity_type = models.ForeignKey(ActivityTypes, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    levels = models.Manager()

    def __str__(self):
        return f'{self.level}'


class ActivityLevel2(models.Model):
    activity_type = models.ForeignKey(ActivityLevel1, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    levels = models.Manager()

    def __str__(self):
        return f'{self.level}'


class ActivityLevel3(models.Model):
    activity_type = models.ForeignKey(ActivityLevel2, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    descript_level = models.TextField(null=True)
    levels = models.Manager()

    def __str__(self):
        return f'{self.level} {self.descript_level}'
