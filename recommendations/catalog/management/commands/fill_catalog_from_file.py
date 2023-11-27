import csv
import os
from more_itertools import unique_everseen
import django
import openpyxl

from django.core.management.base import BaseCommand
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups


class Command(BaseCommand):
    help = "Generate catalog from file."

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendations.settings')
        django.setup()
        workbook = openpyxl.load_workbook('files/dict.xlsx')
        sheet = workbook.active

        def get_set(column: int):
            set_types = set()
            for row in sheet.iter_rows(min_row=2, values_only=True):
                set_types.add(row[column])
            return set_types

        # душа, тело, ум
        set_types = get_set(0)
        for activity in set_types:
            ActivityTypes.types.create(
                activity_type=activity,
            )

        # направление 1
        lst_types = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            full_row = [row[0], row[1], row[2]]
            lst_types.append(full_row)
        lst_types = list(unique_everseen(lst_types))
        for i in range(len(lst_types)):
            ActivityLevel1.levels.create(
                activity_type=ActivityTypes.types.filter(activity_type=lst_types[i][0]).first(),
                id_level=lst_types[i][1],
                level=lst_types[i][2],
            )

        # направление 2
        lst_types = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            full_row = [row[1], row[3], row[4]]
            lst_types.append(full_row)
        lst_types = list(unique_everseen(lst_types))
        for i in range(len(lst_types)):
            ActivityLevel2.levels.create(
                activity_type=ActivityLevel1.levels.filter(id_level=lst_types[i][0]).first(),
                id_level=lst_types[i][1],
                level=lst_types[i][2],
            )
        # направление 3
        lst_types = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            full_row = [row[3], row[5], row[6], row[7]]
            lst_types.append(full_row)
        lst_types = list(unique_everseen(lst_types))
        for i in range(len(lst_types)):
            ActivityLevel3.levels.create(
                activity_type=ActivityLevel2.levels.filter(id_level=lst_types[i][0]).first(),
                id_level=lst_types[i][1],
                level=lst_types[i][2],
                descript_level=lst_types[i][3]
            )

        # группы
        with open('files/groups.csv', 'r', encoding='utf-8') as address_base:
            groups_list = []
            file_reader = csv.reader(address_base, delimiter=',')
            for row in file_reader:
                groups_list.append(row)

            for group in range(1, len(groups_list)):
                Groups.groups.create(
                    uniq_id=groups_list[group][0],
                    level=ActivityLevel3.levels.filter(level=groups_list[group][3]).first(),
                    address=groups_list[group][4],
                    schedule_active=groups_list[group][7],
                    schedule_past=groups_list[group][8],
                    schedule_plan=groups_list[group][9],
                )
                print(group)
