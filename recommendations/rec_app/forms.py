from django import forms

from .models import Question, Choice, ResultOfTest


class AnswerForm(forms.Form):

    def __init__(self, question, user, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.user = user
        choices = []
        self.question = Question.objects.get(pk=question)
        for choice in Choice.objects.all():
            choices.append((choice.votes, choice.choice_text))

        self.fields['choice'] = forms.ChoiceField(
            label=self.question.question_text,
            required=True,
            choices=choices,
            widget=forms.RadioSelect)

    def save(self):
        choice = int(self.cleaned_data['choice'])
        answer = Choice.objects.get(votes=choice)
        if ResultOfTest.objects.filter(user=self.user, question=self.question).exists():
            result = ResultOfTest.objects.get(user=self.user, question=self.question)
            result.answer = answer
            result.save(update_fields=['answer'])
        else:
            result = ResultOfTest(answer=answer, user=self.user, question=self.question)
            result.save()
