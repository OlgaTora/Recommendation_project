import django_filters
from django_filters import CharFilter, filters, ChoiceFilter
from address_book.models import AdministrativeDistrict
from services.weekdays_dict import WEEK_CHOICE

ON_OFF = (('Онлайн', 'Все группы'), ('Оффлайн', 'Только оффлайн'))


class GroupsFilterSearch(django_filters.FilterSet):
    offline = ChoiceFilter(
        choices=ON_OFF,
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
        label='Название улицы',
        method='filter_offline_address')

    weekday = ChoiceFilter(
        choices=WEEK_CHOICE,
        label='День недели',
        method='filter_weekday'
    )

    def filter_offline_address(self, queryset, name, value):
        # только группы оффлайн.
        return queryset.filter(address__icontains=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline_district(self, queryset, name, value):
        # только группы оффлайн.
        return queryset.filter(admin_district=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline(self, queryset, name, value):
        if value != 'Онлайн':
            return queryset.exclude(level__level__icontains='ОНЛАЙН')
        else:
            return queryset

    def filter_weekday(self, queryset, name, value):
        return queryset.filter(weekday=value)


class GroupsFilterCatalog(django_filters.FilterSet):
    districts = filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(),
        label='Район',
        method='filter_district'
    )
    address = CharFilter(
        field_name='address',
        label='Название улицы',
        lookup_expr='icontains')

    weekday = ChoiceFilter(
        choices=WEEK_CHOICE,
        label='День недели',
        method='filter_weekday'
    )

    def filter_district(self, queryset, name, value):
        return queryset.filter(admin_district=value)

    def filter_weekday(self, queryset, name, value):
        return queryset.filter(weekday=value)
