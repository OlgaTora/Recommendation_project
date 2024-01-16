import django_filters
from django_filters import DateTimeFromToRangeFilter, ChoiceFilter, CharFilter

from address_book.models import AdministrativeDistrict
from catalog.models import Groups


# Groups(models.Model):
#     level = models.ForeignKey(ActivityLevel3, on_delete=models.CASCADE)
#     address = models.TextField()
#     districts = models.TextField(null=True)
#     schedule_active = models.TextField(null=True)


class GroupsFilter(django_filters.FilterSet):
    offline = ChoiceFilter()
    # product = CharFilter(field_name='product', lookup_expr='icontains')
    district = ChoiceFilter(choices=list(AdministrativeDistrict.objects.all()))

    # date_created = DateTimeFromToRangeFilter(
    #               widget=django_filters.widgets.RangeWidget(
    #               attrs={'type': 'date'}
    # ))

    class Meta:
        model = Groups
        fields = [
            'district',
        ]
