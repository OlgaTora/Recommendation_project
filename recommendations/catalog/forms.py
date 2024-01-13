from django import forms


class SearchForm(forms.Form):
    search_activity = forms.CharField(max_length=255,  label='Введите название активности')