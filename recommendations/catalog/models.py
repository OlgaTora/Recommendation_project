from django.db import models
from django.db.models import Count

from services.utils import unique_slugify
from users.models import Profile


class ActivityTypes(models.Model):
    activity_type = models.CharField(max_length=255, unique=True, verbose_name='Тип активности')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    def __str__(self):
        return f'{self.activity_type}'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.activity_type)
        super().save(*args, **kwargs)


class ActivityLevel1(models.Model):
    activity_type = models.ForeignKey(ActivityTypes, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    def __str__(self):
        return f'{self.level}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.level)
        super().save(*args, **kwargs)


class ActivityLevel2(models.Model):
    activity_type = models.ForeignKey(ActivityLevel1, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    def __str__(self):
        return f'{self.level}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.level)
        super().save(*args, **kwargs)


class ActivityLevel3(models.Model):
    activity_type = models.ForeignKey(ActivityLevel2, on_delete=models.CASCADE)
    id_level = models.IntegerField()
    level = models.CharField(max_length=255)
    descript_level = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    def __str__(self):
        return f'{self.level}:\n{self.descript_level}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.level)
        super().save(*args, **kwargs)


class Groups(models.Model):
    uniq_id = models.IntegerField()
    level = models.ForeignKey(ActivityLevel3, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.uniq_id}'


class GroupsCorrect(models.Model):
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    level = models.ForeignKey(ActivityLevel3, on_delete=models.CASCADE)
    address = models.TextField()
    admin_district = models.CharField(max_length=255)
    start_date = models.CharField(max_length=32, null=True)
    end_date = models.CharField(max_length=32, null=True)
    weekday = models.CharField(max_length=32, null=True)
    start_time = models.CharField(max_length=32, null=True)
    end_time = models.CharField(max_length=32, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    class Meta:
        ordering = ('-group_id',)

    def __str__(self):
        return f'{self.group_id}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.group_id)
        super().save(*args, **kwargs)

    @staticmethod
    def get_user_groups(user):
        user_groups = Attends.objects.select_related('group_id').filter(user_id=user.pk).distinct()
        return user_groups


class Attends(models.Model):
    uniq_id = models.IntegerField(null=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    online = models.BooleanField()
    date_attend = models.DateField()
    start_time = models.CharField(max_length=32)
    end_time = models.CharField(max_length=32)
    objects = models.Manager()

    def __str__(self):
        return f'{self.uniq_id}'

    @staticmethod
    def get_top_level3(activity_type: ActivityTypes):
        """Function for get top level3 in attends, priority - offline"""
        top_off = Attends.objects.exclude(online='1') \
                      .values('group_id__level') \
                      .annotate(count_level3=Count('group_id__level')) \
                      .order_by('-count_level3')[:10]
        top_offline = ActivityLevel3.objects.filter(
            pk__in=[i.get('group_id__level') for i in top_off])
        level3_offline = top_offline.filter(activity_type__activity_type__activity_type=activity_type)

        top_on = Attends.objects.filter(online='1') \
                     .values('group_id__level') \
                     .annotate(count_level3=Count('group_id__level')) \
                     .order_by('-count_level3')[:5]
        top_online = ActivityLevel3.objects.filter(
            pk__in=[i.get('group_id__level') for i in top_on])
        level3_online = top_online.filter(activity_type__activity_type__activity_type=activity_type)

        # если нет level3 по этому типу активности в топе
        if not level3_online.exists() and not level3_offline.exists():
            return top_offline, top_online
        return level3_offline, level3_online
