from django.db import models
from smart_selects.db_fields import ChainedForeignKey


class AdministrativeDistrict(models.Model):
    admin_district_name = models.CharField(max_length=255, verbose_name='Название округа')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Округ'

    def __str__(self):
        return f'{self.admin_district_name}'


class District(models.Model):
    admin_district = models.ForeignKey(AdministrativeDistrict, on_delete=models.CASCADE, default=None)
    district_name = models.CharField(max_length=255)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Район'

    def __str__(self):
        return f'{self.district_name}'


class StreetType(models.Model):
    street_type = models.CharField(max_length=255)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Тип улицы'

    def __str__(self):
        return f'{self.street_type}'


class Streets(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=None)
    street_type = models.ForeignKey(StreetType, on_delete=models.CASCADE, default=None)
    street_name = models.CharField(max_length=255)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Улица'

    def __str__(self):
        return f'{self.street_name} {self.street_type}'


class StreetsBook(models.Model):
    admin_district = models.ForeignKey(
        AdministrativeDistrict,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Округ'
    )
    district = ChainedForeignKey(
        District,
        chained_field='admin_district',
        chained_model_field='admin_district',
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Район'
    )
    street_name = ChainedForeignKey(
        Streets,
        chained_field='district',
        chained_model_field='district',
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Улица'
    )
    street_type = models.ForeignKey(StreetType, on_delete=models.CASCADE, default=None)
    index = models.CharField(max_length=255)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Адресная книга'
