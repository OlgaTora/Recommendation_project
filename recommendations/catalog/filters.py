import django_filters
from django_filters import CharFilter, filters, ChoiceFilter
from address_book.models import AdministrativeDistrict
from services.dictionaries import WEEK_CHOICE, ON_OFF, TIME_CHOICE


class GroupsFilter(django_filters.FilterSet):
    districts = filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(),
        label='Район',
        method='filter_district'
    )
    address = CharFilter(
        label='Название улицы',
        lookup_expr='icontains')
    weekday = ChoiceFilter(
        choices=WEEK_CHOICE,
        label='День недели',
        method='filter_weekday'
    )
    start_time = ChoiceFilter(
        choices=TIME_CHOICE,
        label='Время начала',
        method='filter_time'
    )

    def filter_weekday(self, queryset, name, value):
        return queryset.filter(weekday=value)

    def filter_time(self, queryset, name, value):
        return queryset.filter(start_time__icontains=value)


class GroupsFilterSearch(GroupsFilter):
    offline = ChoiceFilter(
        choices=ON_OFF,
        label='Онлайн/Оффлайн',
        method='filter_offline'
    )

    address = CharFilter(
        label='Название улицы',
        method='filter_address')

    def filter_address(self, queryset, name, value):
        # только группы оффлайн.
        return queryset.filter(address__icontains=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_district(self, queryset, name, value):
        # только группы оффлайн.
        return queryset.filter(admin_district=value).exclude(level__level__icontains='ОНЛАЙН')

    def filter_offline(self, queryset, name, value):
        if value != 'Онлайн':
            return queryset.exclude(level__level__icontains='ОНЛАЙН')
        else:
            return queryset


class GroupsFilterCatalog(GroupsFilter):

    def filter_district(self, queryset, name, value):
        return queryset.filter(admin_district=value)
