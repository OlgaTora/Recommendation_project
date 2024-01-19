from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
import datetime as DT

from data_transform.weekdays_dict import WEEKDAYS_DICT

from catalog.models import Attends, Groups
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
        period = []
        weekdays_time_choices = []
        lst = group.extract
        for i in lst:
            res = f'{i[2]} {i[3]}'
            weekdays_time_choices.append((res, res))
            period.append(DT.datetime.strptime(i[0], '%d.%m.%Y'))
            period.append(DT.datetime.strptime(i[1], '%d.%m.%Y'))

        start_date = min(period)
        end_date = max(period)

        self.fields['weekday_choice'] = forms.ChoiceField(
            label='Выберите подходящий день недели и время:',
            required=True,
            choices=weekdays_time_choices,
            widget=forms.RadioSelect)

        self.fields['date_choice'] = forms.DateField(
            label='Выберите подходящую дату:',
            required=True,
            widget=DatePickerInput(
                options={
                    'minDate': start_date.strftime('%Y-%m-%d 00:00:00'),
                    'maxDate': end_date.strftime('%Y-%m-%d 00:00:00'),
                }
            )
        )

    def clean(self):
        data = self.cleaned_data
        date_choice = data.get('date_choice')
        weekday_choice = data.get('weekday_choice')
        if weekday_choice:
            weekday = date_choice.weekday()
            weekday_choice = int(WEEKDAYS_DICT[weekday_choice[:2]])
            if weekday_choice != weekday:
                raise forms.ValidationError('День недели должен совпадать с выбранным.')
        return data

    def save(self):
        attend = Attends(
            group_id=Groups.objects.get(pk=self.group.pk),
            user_id=Profile.objects.get(pk=self.user.pk),
            online=True if 'ОНЛАЙН' in self.group.level.descript_level else False,
            date_attend=self.cleaned_data['date_choice'],
            start_time=self.cleaned_data['weekday_choice'][3:8],
            end_time=self.cleaned_data['weekday_choice'][9:],
        )
        attend.save()
