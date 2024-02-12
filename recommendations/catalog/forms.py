from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
import datetime as dt

from catalog.models import Attends, Groups
from services.dictionaries import WEEKDAYS_DICT
from users.models import Profile


class SearchForm(forms.Form):
    search_activity = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""


class DateTimeChoiceForm(forms.Form):
    def __init__(self, *args, group, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.user = user
        self.fields['date_choice'] = forms.DateField(
            label='Выберите подходящую дату:',
            required=True,
            widget=DatePickerInput(
                options={
                    'format': 'DD.MM.YYYY',
                    'minDate': dt.datetime.strptime(self.group.start_date, '%d.%m.%Y'),
                    'maxDate': dt.datetime.strptime(self.group.end_date, '%d.%m.%Y'),
                }
            )
        )

    def clean(self):
        data = self.cleaned_data
        date_choice = data.get('date_choice')
        if date_choice:
            weekday_choice = date_choice.weekday()
            weekday = int(WEEKDAYS_DICT[self.group.weekday])
            if weekday_choice != weekday:
                raise forms.ValidationError('День недели должен совпадать с выбранным.')
        return data

    def save(self):
        attend = Attends(
            group_id=Groups.objects.get(pk=self.group.group_id.pk),
            user_id=Profile.objects.get(pk=self.user.pk),
            online=True if 'ОНЛАЙН' in self.group.level.level else False,
            date_attend=self.cleaned_data['date_choice'],
            start_time=self.group.start_time,
            end_time=self.group.end_time,
        )
        attend.save()
