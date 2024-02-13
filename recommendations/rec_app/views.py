from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView
from django_filters.views import FilterView

from address_book.models import StreetsBook
from catalog.filters import GroupsFilterSearch
from catalog.models import Groups, ActivityTypes, Attends, GroupsCorrect
from .forms import AnswerForm
from .models import Question, ResultOfTest, TestResultDescription, VotesGroups
from django.contrib import messages


class RecommendationView(LoginRequiredMixin, FilterView):
    """
    Recommendation based on test results and user address
    """
    result: int | None
    template_name = 'rec_app/recommendations.html'
    extra_context = {'message': 'Выберите занятие:',
                     'message_error': 'Мы ничего не нашли по вашему запросу'}
    redirect_field_name = reverse_lazy('users:index')
    model = GroupsCorrect
    paginate_by = 10
    context_object_name = 'groups_list'
    filterset_class = GroupsFilterSearch

    def get_result(self):
        if not hasattr(self, 'result'):
            self.result = ResultOfTest.get_results(self.request.user)
        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.get_result()

        # !!!!  user_groups = Attends.objects.select_related('group_id').filter(user_id=user.pk).distinct()

        votes_group = VotesGroups.objects.get(votes=result)
        context['result'] = result
        context['description'] = TestResultDescription.objects.get(pk=votes_group.result_group.pk)
        return context

    def get(self, request, *args, **kwargs):
        result = self.get_result()
        if result is None:
            messages.error(
                self.request,
                'Вы ответили не на все вопросы, начните тестирование с начала.'
            )
            return redirect(reverse('rec_app:question_and_answers', args=(1,)))
        return super(RecommendationView, self).get(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        votes_group = VotesGroups.objects.get(votes=self.get_result())
        activity_type = ActivityTypes.objects.get(pk=votes_group.result_group.pk)
        # топ offline & online
        level3_offline, level3_online = Attends.get_top_level3(activity_type)
        groups_list_on = GroupsCorrect.objects.filter(level__in=level3_online) \
            .exclude(start_date='')
        groups_list_off = GroupsCorrect.objects.filter(level__in=level3_offline) \
            .exclude(start_date='')
        user_groups = GroupsCorrect.get_user_groups(self.request.user)
        user_address = self.request.user.address
        if user_address:
            admin_districts = StreetsBook.admin_districts_transform(user_address)
            tmp = Groups.objects.none()
            for i in range(len(admin_districts)):
                groups = groups_list_off.filter(
                    admin_district=admin_districts[i])
                tmp = tmp | groups
            groups_list_off = tmp
        groups_list = groups_list_off | groups_list_on
        queryset = groups_list.exclude(pk__in=user_groups)
        return queryset


class QuestionFormView(LoginRequiredMixin, FormView):
    """
    Testing user
    """
    template_name = 'rec_app/test_form.html'
    extra_context = {'message': 'Для получения рекомендаций ответьте, пожалуйста, на все вопросы.'}
    form_class = AnswerForm
    redirect_field_name = reverse_lazy('users:index')
    success_url = 'rec_app:recommendations'
    question: int

    def get_question(self):
        if not hasattr(self, 'question'):
            self.question = self.kwargs.get('question')
        return self.question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.get_question()).pk
        return context

    def get(self, request, *args, **kwargs):
        last_page = Question.objects.latest('pk').pk + 1
        # когда ответил на последний вопрос
        if self.get_question() == last_page:
            votes = len(ResultOfTest.objects.filter(user=request.user)
                        .annotate(count=Count('user')))
            if votes == last_page - 1:
                return redirect(self.get_success_url())
            else:
                messages.error(request, 'Вы ответили не на все вопросы,'
                                        ' начните тестирование с начала.')
                return redirect(reverse('rec_app:question_and_answers', args=(1,)))
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        kwargs = super(QuestionFormView, self).get_form_kwargs()
        kwargs['question'] = self.get_question()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        question = self.get_question() + 1
        return redirect(reverse('rec_app:question_and_answers', args=(question,)))


class StartView(LoginRequiredMixin, TemplateView):
    """
    Start test
    """
    redirect_field_name = reverse_lazy('users:index')

    def get(self, request, *args, **kwargs):
        results = ResultOfTest.objects.filter(user=request.user)
        if results.exists():
            if results.count() < Question.objects.latest('pk').pk:
                results.delete()
                return redirect(reverse('rec_app:question_and_answers', args=(1,)))
            else:
                return redirect(reverse('rec_app:restart_test'))
        return redirect(reverse('rec_app:question_and_answers', args=(1,)))


class RestartView(LoginRequiredMixin, TemplateView):
    """
    Choice: results or restart test
    """
    redirect_field_name = reverse_lazy('users:index')

    def get(self, request, *args, **kwargs):
        if ResultOfTest.objects.filter(user=request.user).exists():
            return render(request, 'rec_app/restart_test.html')
        else:
            return redirect(reverse('rec_app:start_test'))
