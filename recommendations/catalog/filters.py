import django_filters
from django_filters import DateTimeFromToRangeFilter, CharFilter, filters, BooleanFilter
from django_filters.widgets import BooleanWidget
from django.utils.translation import gettext as _
from address_book.models import AdministrativeDistrict
from catalog.models import Groups


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("False", _("Все занятия")), ("True", _("Только оффлайн")))


class GroupsFilterSearch(django_filters.FilterSet):
    offline = BooleanFilter(
        widget=CustomBooleanWidget(),
        label='Онлайн/Оффлайн',
        method='filter_offline'
    )

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
        return queryset.filter(districts__icontains=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline(self, queryset, name, value):
        return queryset.exclude(level__level__icontains='ОНЛАЙН')

    # date = DateTimeFromToRangeFilter(
    #               widget=django_filters.widgets.RangeWidget(
    #               attrs={'type': 'date'}
    # )

    class Meta:
        model = Groups
        fields = ['address', 'districts']


class GroupsFilterCatalog(django_filters.FilterSet):
    districts = filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(),
        label='Район',
    )
    address = CharFilter(
        field_name='address',
        label='Адрес',
        lookup_expr='icontains')

    # date = DateTimeFromToRangeFilter(
    #               widget=django_filters.widgets.RangeWidget(
    #               attrs={'type': 'date'}
    # )

    class Meta:
        model = Groups
        fields = [
            'address',
            'districts'
        ]