import csv
import os
import django

from django.core.management.base import BaseCommand
from more_itertools import unique_everseen

from address_book.models import StreetsBook, District, AdministrativeDistrict, StreetType, Streets


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
        district_list = set()
        street_types_list = set()
        street_names_list = set()

        for row in address_list:
            admin_district_list.add(row[3])
            full_row_district = (row[3], row[4])
            district_list.add(full_row_district)
            street_types_list.add(row[1])
            street_names_list.add(row[0])

        # # fill admin districts
        # for admin_district in admin_district_list:
        #     AdministrativeDistrict.admin_districts.create(
        #         admin_district_name=admin_district,
        #     )
        #
        # # fill street types
        # for street_type in street_types_list:
        #     StreetType.street_types.create(
        #         street_type=street_type,
        #     )
        #
        # fill districts
        # for district in district_list:
        #     District.districts.create(
        #         admin_district=AdministrativeDistrict.admin_districts.get(admin_district_name=district[0]),
        #         district_name=district[1]
        #     )
        # # district_list = list(unique_everseen(district_list))
        #
        # # fill streets
        # for street in street_names_list:
        #     Streets.streets.create(
        #         street_name=street
        #     )

        for address in range(len(address_list)):
            admin_district = AdministrativeDistrict.admin_districts.get(admin_district_name=address_list[address][3])
            district = District.districts.get(district_name=address_list[address][4])
            street_type = StreetType.street_types.get(street_type=address_list[address][1])
            street_name = Streets.streets.get(street_name=address_list[address][0],
                                              street_name__contains=address_list[address][0])

            StreetsBook.streets_book.create(
                admin_district=admin_district,
                district=district,
                street_type=street_type,
                street_name=street_name,
                index=address_list[address][2]
            )
