import django_filters
from django.forms import CheckboxInput
from django_filters import CharFilter, filters, BooleanFilter, ChoiceFilter
from django_filters.widgets import BooleanWidget
from django.utils.translation import gettext as _
from address_book.models import AdministrativeDistrict
from catalog.models import Groups

# class CustomBooleanWidget(BooleanWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.choices = (("", _("--------")),("False", _("Все занятия")), ("True", _("Только оффлайн")))

CHOICES = (('Онлайн', 'Все занятия'), ('Оффлайн', 'Только оффлайн'))


class GroupsFilterSearch(django_filters.FilterSet):
    offline = ChoiceFilter(
        choices=CHOICES,
        label='Онлайн/Оффлайн',
        method='filter_offline'
    )

    # offline = BooleanFilter(
    #     widget=CustomBooleanWidget(),
    #     label='Онлайн/Оффлайн',
    #     method='filter_offline'
    # )

    districts = filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(),
        label='Район',
        method='filter_offline_district'
    )
    address = CharFilter(
        field_name='address',
        label='Адрес',
        method='filter_offline_address')

    def filter_offline_address(self, queryset, name, value):
        # только группы оффлайн.
        return queryset.filter(address__icontains=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline_district(self, queryset, name, value):
        # только группы оффлайн.
        value = f'{str(value).split(" ")[0]}'
        return queryset.filter(districts__icontains=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline(self, queryset, name, value):
        #print(value)
        #return queryset.exclude(level__level__icontains='ОНЛАЙН')
        if value != 'Онлайн':
            print('aa')
            return queryset.exclude(level__level__icontains='ОНЛАЙН')
        else:
            return queryset

    class Meta:
        model = Groups
        fields = ['address', 'districts', ]


class GroupsFilterCatalog(django_filters.FilterSet):
    districts = filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(),
        label='Район',
        method='filter_district'
    )
    address = CharFilter(
        field_name='address',
        label='Адрес',
        lookup_expr='icontains')

    def filter_district(self, queryset, name, value):
        value = f'{str(value).split(" ")[0]}'
        return queryset.filter(districts__icontains=value)

    class Meta:
        model = Groups
        fields = [
            'address',
            'districts',
        ]
