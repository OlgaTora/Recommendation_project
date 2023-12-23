from django.db import models

from data_transform.street_types_dict import street_types_dict


class AdministrativeDistrict(models.Model):
    admin_district_name = models.CharField(max_length=255)
    admin_districts = models.Manager()

    def __str__(self):
        return f'{self.admin_district_name}'


class District(models.Model):
    admin_district = models.ForeignKey(AdministrativeDistrict, on_delete=models.CASCADE, default=None)
    district_name = models.CharField(max_length=255)
    districts = models.Manager()

    def __str__(self):
        return f'{self.district_name}'


class StreetType(models.Model):
    street_type = models.CharField(max_length=255)
    street_types = models.Manager()

    def __str__(self):
        return f'{self.street_type}'


class StreetsBook(models.Model):
    street_type = models.ForeignKey(StreetType, on_delete=models.CASCADE, default=None)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=None)
    street_name = models.CharField(max_length=255)
    index = models.CharField(max_length=255)
    streets = models.Manager()

    def __str__(self):
        return f'{self.street_name}'

    @staticmethod
    def address_transform(address: str):
        """Funcion for check user address in address book"""
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
        address = address.title()
        if street_type:
            user_address = (
                StreetsBook.streets.filter(street_name=address,
                                           street_type=StreetType.street_types.get(street_type=street_type)
                                           ))
        else:
            user_address = (StreetsBook.streets.filter(street_name=address))
        return user_address

