from django import forms


class SearchForm(forms.Form):
    search_activity = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""


class DateTimeChoiceForm(forms.Form):
    def __init__(self, *args, group, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        dct = group.extract
        print(dct)
        time_choices = []
        weekdays_choices = []
        dates_choices = []

        # for key, value in dct.items():
        #
        #     for i in value:
        #         for key, value in i.items():
        #             time_list.append(str(value))
        # return time_list

        dates_period = group.extract_period[0]
        import datetime as DT
        import pandas as pd
        dates_period = dates_period.split('-')
        print(dates_period)

        start_date = DT.datetime.strptime(dates_period[0], '%d.%m.%Y')
        end_date = DT.datetime.strptime(dates_period[1], '%d.%m.%Y')
        dates_choices = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d.%m.%Y').tolist()

        for choice in set(group.extract_weekdays):
            weekdays_choices.append((choice, choice))
        for choice in group.extract_time:
            time_choices.append((choice, choice))
        for choice in dates_choices:
            dates_choices.append((choice, choice))

        self.fields['time_choice'] = forms.ChoiceField(
            label='Time',
            required=True,
            choices=time_choices,
            widget=forms.RadioSelect)

        self.fields['weekday_choice'] = forms.ChoiceField(
            label='Day',
            required=True,
            choices=weekdays_choices,
            widget=forms.RadioSelect)

        self.fields['date_choice'] = forms.ChoiceField(
            label='Date',
            required=True,
            choices=dates_choices,)
        #
        # def save(self):
        #     choice = int(self.cleaned_data['choice'])
        #     answer = Choice.choices.get(votes=choice)
        #     result = ResultOfTest(answer=answer, user=self.user, question=self.question)
        #     result.save()
