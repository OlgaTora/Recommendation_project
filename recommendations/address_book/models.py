from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from services.address_parser.street_types_dict import street_types_dict


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

    @staticmethod
    def address_transform(address: str):
        address = str(address)
        """Function for check user address in address book"""
        street_type = ''
        # если адрес - одно слово
        if len(address.split(',')) != 1:
            address = address.split(',')[1].strip()
            # если можно выделить улицу и дом
            if len(address.split()) != 1:
                tmp = address.split()
                for word in tmp:
                    for key, value in street_types_dict.items():
                        if word in value:
                            street_type = key
                            tmp.remove(word)
                            address = (' '.join(tmp))
        if street_type:
            street_names = Streets.objects.filter(
                street_name=address,
                street_type=StreetType.objects.get(street_type=street_type))
            user_address = StreetsBook.objects.filter(
                street_name__in=street_names,
                street_type=StreetType.objects.get(street_type=street_type)
            )
        else:
            street_names = Streets.objects.filter(street_name=address)
            user_address = StreetsBook.objects.filter(street_name__in=street_names)
        return user_address

    @staticmethod
    def admin_districts_transform(address: str) -> list:
        # адрес пользователя: так как нет инфо по району пользователя, берем все улицы с таким названием
        user_address = list(StreetsBook.address_transform(address))
        admin_districts = list(set([i.admin_district.admin_district_name for i in user_address]))
        admin_districts = [str(i).split(" ")[0] for i in admin_districts]
        return admin_districts
