from django.db import models


class ActivityTypes(models.Model):
    activity_type = models.CharField(max_length=255, unique=True)
    types = models.Manager()

    def __str__(self):
        return f'{self.activity_type}'

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
        return f'{self.level}\n{self.descript_level}'


class Groups(models.Model):
    uniq_id = models.IntegerField()
    level = models.ForeignKey(ActivityLevel3, on_delete=models.CASCADE)
    address = models.TextField()
    districts = models.TextField(null=True)
    schedule_active = models.TextField(null=True)
    schedule_past = models.TextField(null=True)
    schedule_plan = models.TextField(null=True)
    groups = models.Manager()

    def __str__(self):
        return f'{self.level}'
