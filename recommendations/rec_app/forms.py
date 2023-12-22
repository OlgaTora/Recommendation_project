from django import forms

from address_book.models import AdministrativeDistrict
from .models import Question, Choice, ResultOfTest


class AnswerForm(forms.Form):
    def __init__(self, *args, page_num, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page_num
        self.user = user
        choices = []
        question_pk = self.page
        self.question = Question.questions.get(pk=question_pk)
        for choice in Choice.choices.all():
            choices.append((choice.votes, choice.choice_text))

        self.fields['choice'] = forms.ChoiceField(
            label=self.question.question_text,
            required=True,
            choices=choices,
            widget=forms.RadioSelect)

    def save(self):
        choice = int(self.cleaned_data['choice'])
        answer = Choice.choices.get(votes=choice)
        result = ResultOfTest(answer=answer, user=self.user, question=self.question)
        result.save()

