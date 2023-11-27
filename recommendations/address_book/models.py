from django.db import models


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
