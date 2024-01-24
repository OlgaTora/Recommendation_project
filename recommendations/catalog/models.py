from django.db import models
from django.db.models import Count
from django.urls import reverse

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
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.activity_type)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('types', kwargs={'type_slug': self.slug})


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

    def get_absolute_url(self):
        return reverse('level1', kwargs={'level_slug': self.slug})


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

    def get_absolute_url(self):
        return reverse('level2', kwargs={'level_slug': self.slug})


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

    def get_absolute_url(self):
        return reverse('level3', kwargs={'level_slug': self.slug})


class Groups(models.Model):
    uniq_id = models.IntegerField()
    level = models.ForeignKey(ActivityLevel3, on_delete=models.CASCADE)
    address = models.TextField()
    districts = models.TextField(null=True)
    schedule_active = models.TextField(null=True)
    schedule_past = models.TextField(null=True)
    schedule_plan = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    class Meta:
        ordering = ('-uniq_id',)

    def __str__(self):
        return f'{self.level}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.uniq_id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups', kwargs={'groups_slug': self.slug})

    @property
    def extract(self):
        s = str(self.schedule_active)
        result = []
        if s.count(';') == 0:
            if s.count('перерыв') > 1:
                result = case_two_dates_two_time(s)
            else:
                result = case_one_time(s)
        else:
            """
            обработка случая 'c 01.06.2022 по 11.08.2022, Пн., Ср. 12:05-13:05, без перерыва;
            c 01.01.2022 по 31.05.2022, Пн., Ср. 12:15-13:15, без перерыва;
            """
            spl = [i.strip() for i in s.split(';')]
            for lst in spl:
                if lst.count('перерыв') > 1:
                    lst = case_two_dates_two_time(lst)
                    result += lst
                else:
                    lst = case_one_time(lst)
                    result += lst
        return result


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
    def get_top_level3():
        """Function for get top level3 in attends"""
        top_off = Attends.objects.exclude(online='1') \
                      .values('group_id__level') \
                      .annotate(count_level3=Count('group_id__level')) \
                      .order_by('-count_level3')[:10]
        levels3_off = ActivityLevel3.objects.filter(pk__in=[i.get('group_id__level') for i in top_off])
        top_on = Attends.objects.filter(online='1') \
                     .values('group_id__level') \
                     .annotate(count_level3=Count('group_id__level')) \
                     .order_by('-count_level3')[:10]
        levels3_on = ActivityLevel3.objects.filter(pk__in=[i.get('group_id__level') for i in top_on])
        return levels3_off, levels3_on


def clean_str(s: str):
    str_clean = (s.replace('c', '')
                 .replace('по', '')
                 .replace('без перерыва', '')
                 .replace(',', '')).strip()
    return str_clean


def case_one_time(s: str):
    """
    обработка случая 'c 31.03.2023 по 31.12.2023, Пн., Ср. 17:00-19:00, без перерыва'
    """
    str_clean = clean_str(s)
    spl = [i for i in str_clean.split(' ')]
    lst = []
    schedule_dict = extract_time_weekday(spl)
    if schedule_dict:
        for day, times in schedule_dict.items():
            lst.append([spl[0], spl[2], day, times])
    return lst


def case_two_dates_two_time(s: str):
    """
    обработка случая 'c 31.03.2023 по 31.12.2023, Вт. 17:00-19:00, без перерыва, Пт. 13:00-15:00, без перерыва'
    """
    str_split = s.split('без перерыва')
    str_clean = clean_str(str_split[0])
    spl = [i for i in str_clean.split(' ')]
    lst = []
    schedule_dict = extract_time_weekday(spl)
    if schedule_dict:
        for day, times in schedule_dict.items():
            lst.append([spl[0], spl[2], day, times])
    for i in range(1, len(str_split)):
        new_str_split = [i for i in clean_str(str_split[i]).split(' ')]
        schedule_dict_ = extract_time_weekday(new_str_split)
        if schedule_dict_:
            for day_, times_ in schedule_dict_.items():
                lst.append([spl[0], spl[2], day_, times_])
    return lst


def extract_time_weekday(elem: list):
    weeksdays_list = ['Пн.', 'Вт.', 'Ср.', 'Чт.', 'Пт.', 'Сб.', 'Вс.']
    times = []
    weeksdays = []
    schedule_dict = {}
    for j in elem:
        if j in weeksdays_list:
            weeksdays.append(j[:-1])
        if '-' in j:
            times.append(j)
    if len(weeksdays) == len(times):
        schedule_dict = dict(zip(weeksdays, times))
    elif len(weeksdays) > len(times):
        for i in weeksdays:
            schedule_dict[i] = times[0]
    else:
        for i in times:
            times[i] = weeksdays
    if schedule_dict:
        return schedule_dict
