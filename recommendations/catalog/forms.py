from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
import datetime as dt

from catalog.models import Attends, Groups, GroupsCorrect
from services.dictionaries import WEEKDAYS_DICT
from users.models import Profile


class SearchForm(forms.Form):
    search_activity = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""


class DateTimeChoiceForm(forms.Form):
    def __init__(self, *args, group_pk, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_pk = group_pk
        group = GroupsCorrect.objects.get(pk=self.group_pk)
        self.user = user
        self.fields['date_choice'] = forms.DateField(
            label='Выберите подходящую дату:',
            required=True,
            widget=DatePickerInput(
                options={
                    'format': 'DD.MM.YYYY',
                    'minDate': dt.datetime.strptime(group.start_date, '%d.%m.%Y'),
                    'maxDate': dt.datetime.strptime(group.end_date, '%d.%m.%Y'),
                }
            )
        )

    def clean(self):
        data = self.cleaned_data
        group = GroupsCorrect.objects.get(pk=self.group_pk)
        date_choice = data.get('date_choice')
        if date_choice:
            weekday_choice = date_choice.weekday()
            weekday = int(WEEKDAYS_DICT[group.weekday])
            if weekday_choice != weekday:
                raise forms.ValidationError('День недели должен совпадать с выбранным.')
        return data

    def save(self):
        group = GroupsCorrect.objects.get(pk=self.group_pk)
        attend = Attends(
            group_id=Groups.objects.get(pk=group.group_id.pk),
            user_id=Profile.objects.get(pk=self.user.pk),
            online=True if 'ОНЛАЙН' in group.group_id.level.level else False,
            date_attend=self.cleaned_data['date_choice'],
            start_time=group.start_time,
            end_time=group.end_time,
        )
        attend.save()
