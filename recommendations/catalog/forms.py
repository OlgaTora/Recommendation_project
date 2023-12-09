from django import forms


class SearchForm(forms.Form):
    search_activity = forms.CharField(max_length=255, label='Введите название активности')
    #
    # def clean(self, *args, **kwargs):
    #     search_activity = self.cleaned_data['search_activity']
    #     return search_activity
