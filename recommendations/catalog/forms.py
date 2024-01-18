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

        weekdays_time_choices = []
        lst = group.extract
        print(lst)
        for i in lst:
            res = ''
            i = i[0].split(',')
            for j in i:
                res += f'{j}'
            #     res = f"{j[1]} {j[2]}"
            print(res)
            weekdays_time_choices.append((res, res))

        import datetime as DT
        import pandas as pd
        # dates_period = dates_period.split('-')
        # print(dates_period)

        # start_date = DT.datetime.strptime(dates_period[0], '%d.%m.%Y')
        # end_date = DT.datetime.strptime(dates_period[1], '%d.%m.%Y')
        # dates_choices = pd.date_range(
        #     min(start_date, end_date),
        #     max(start_date, end_date)
        # ).strftime('%d.%m.%Y').tolist()

        # for choice in dates_choices:
        #     dates_choices.append((choice, choice))

        self.fields['weekday_choice'] = forms.ChoiceField(
            label='Day and time',
            required=True,
            choices=weekdays_time_choices,
            widget=forms.RadioSelect)

        # self.fields['date_choice'] = forms.ChoiceField(
        #     label='Date',
        #     required=True,
        #     choices=dates_choices,)
        #
        # def save(self):
        #     choice = int(self.cleaned_data['choice'])
        #     answer = Choice.choices.get(votes=choice)
        #     result = ResultOfTest(answer=answer, user=self.user, question=self.question)
        #     result.save()
