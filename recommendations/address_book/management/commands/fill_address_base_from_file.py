import csv
import os
import django

from django.core.management.base import BaseCommand
from more_itertools import unique_everseen

from address_book.models import StreetsBook, District, AdministrativeDistrict, StreetType


class Command(BaseCommand):
    help = "Generate catalog from file."

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()

        with open('files/moscow_streets.csv', 'r', encoding='utf-8') as address_base:
            address_list = []
            file_reader = csv.reader(address_base, delimiter=',')
            next(file_reader)
            for row in file_reader:
                address_list.append(row)

        admin_district_list = set()
        district_list = []
        street_types_list = set()

        for row in address_list:
            admin_district_list.add(row[3])
            full_row_district = [row[3], row[4]]
            district_list.append(full_row_district)
            street_types_list.add(row[1])

        # fill admin districts
        for admin_district in admin_district_list:
            AdministrativeDistrict.admin_districts.create(
                admin_district_name=admin_district,
            )

        # fill street types
        for street_type in street_types_list:
            StreetType.street_types.create(
                street_type=street_type,
            )

        # fill districts
        district_list = list(unique_everseen(district_list))
        for district in range(len(district_list)):
            admin_district = AdministrativeDistrict.admin_districts.filter(
                admin_district_name=district_list[district][0]).first()
            District.districts.create(
                admin_district=admin_district,
                district_name=district_list[district][1],
            )
        # fill streets
        # for street in range(len(address_list)):
        #     district = District.districts.filter(
        #         district_name=address_list[street][4]).first()
        #     street_type = StreetType.street_types.filter(street_type=address_list[street][1]).first()
        #     StreetsBook.streets.create(
        #         district=district,
        #         street_type=street_type,
        #         street_name=address_list[street][0],
        #         index=address_list[street][2]
        #     )
