from django.db import models
from django.db.models import Count

from users.models import Profile


class ActivityTypes(models.Model):
    activity_type = models.CharField(max_length=255, unique=True, verbose_name='Тип активности')
    types = models.Manager()

    # slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

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


class Attends(models.Model):
    uniq_id = models.IntegerField()
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    online = models.BooleanField()
    date_attend = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    attends = models.Manager()

    def __str__(self):
        return f'{self.uniq_id}'

    @staticmethod
    def get_top_level3():
        """Function for get top-10 level3 in attends"""
        top = Attends.attends.values('group_id__level') \
                  .annotate(count_level3=Count('group_id__level')) \
                  .order_by('-count_level3')[:10]
        levels3 = ActivityLevel3.levels.filter(pk__in=[i.get('group_id__level') for i in top])
        return levels3
