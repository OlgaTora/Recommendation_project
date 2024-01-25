from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.views import View

from address_book.models import StreetsBook
from catalog.filters import GroupsFilterSearch
from catalog.models import Groups, ActivityTypes, Attends
from .forms import AnswerForm
from .models import Question, ResultOfTest, TestResultDescription, VotesGroups
from django.contrib import messages


@login_required(redirect_field_name='/')
def recommendations(request):
    """Recommendation based on test results and user address"""
    result = ResultOfTest.get_results(request.user)
    votes_group = VotesGroups.objects.get(votes=result)
    description = TestResultDescription.objects.get(pk=votes_group.result_group.pk)
    activity_type = ActivityTypes.objects.get(pk=description.activity_type.pk)
    # топ offline-10, online-5
    level3_offline, level3_online = Attends.get_top_level3(activity_type)

    user_address = request.user.address
    groups_list_on = Groups.objects.filter(level__in=level3_online).exclude(schedule_active='')
    print(f'len group list on={len(groups_list_on)}')
    # если адрес есть в базе адресов Москвы
    if user_address:
        admin_districts = StreetsBook.admin_districts_transform(user_address)
        # группы по типу активности из теста и из района пользователя
        groups_list_off = (Groups.objects.filter(
            level__in=level3_offline,
            districts__icontains=admin_districts[0])
                           .exclude(schedule_active=''))
        print(f'len group list {admin_districts[0]}={len(groups_list_off)}')
        # если улица с этим названием в нескольких районах
        if len(admin_districts) > 1:
            for i in range(1, len(admin_districts)):
                groups = (Groups.objects.filter(
                    level__in=level3_offline,
                    districts__icontains=admin_districts[i])
                          .exclude(schedule_active=''))
                print(f'len group {admin_districts[i]}={len(groups)}')
                groups_list_off = groups_list_off | groups
                print(f'len group list off={len(groups_list_off)}')
        groups_list = groups_list_off | groups_list_on
    else:
        groups_list = groups_list_on
    print(f'len group list={len(groups_list)}')

    user_groups = Groups.get_user_groups(request.user)
    print(f'len user_groups={len(user_groups)}')
    groups_list = groups_list.exclude(pk__in=user_groups)
    print(f'len group list after filter={len(groups_list)}')

    group_filter = GroupsFilterSearch(request.GET, queryset=groups_list)
    groups_list = group_filter.qs
    paginator = Paginator(groups_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'rec_app/recommendations.html',
                  {'result': result,
                   'description': description,
                   'group_filter': group_filter,
                   'groups_list': page_obj})


@login_required(redirect_field_name='/')
def question_form(request, page_num=1):
    """Testing"""
    message = 'Для получения рекомендаций ответьте, пожалуйста, на все вопросы.'
    last_page = int(Question.objects.latest('pk').pk) + 1
    user = request.user
    if page_num > last_page:
        return render(request, '404.html')

    # когда ответил на последний вопрос
    if page_num == last_page:
        votes = len(ResultOfTest.objects.filter(user=user).annotate(count=Count('user')))
        if votes >= last_page - 1:
            return redirect('rec_app:recommendations')
        else:
            messages.error(request, 'Вы ответили не на все вопросы, начните тестирование с начала.')
            return redirect(reverse('rec_app:question_and_answers', args=(1,)))

    question = get_object_or_404(Question, pk=page_num)
    form = AnswerForm(request.POST or None, page_num=page_num, user=user)
    if form.is_valid():
        form.save()
        page_num += 1
        return redirect(reverse('rec_app:question_and_answers', args=(page_num,)))
    return render(request,
                  'rec_app/test_form.html',
                  {'form': form, 'pk': question.pk, 'message': message})


class StartView(LoginRequiredMixin, View):
    """Start test"""
    redirect_field_name = reverse_lazy('users:index')

    def get(self, request, *args, **kwargs):
        results = ResultOfTest.objects.filter(user=request.user)
        if results.exists():
            if results.count() < 10:
                results.delete()
                return redirect(reverse('rec_app:question_and_answers', args=(1,)))
            else:
                return redirect(reverse('rec_app:restart_test'))
        return redirect(reverse('rec_app:question_and_answers', args=(1,)))


class RestartView(LoginRequiredMixin, View):
    """Choice: results or restart test"""
    redirect_field_name = reverse_lazy('users:index')

    def get(self, request, *args, **kwargs):
        if ResultOfTest.objects.filter(user=request.user).exists():
            return render(request, 'rec_app/restart_test.html')
        else:
            return redirect(reverse('rec_app:start_test'))
#
# @login_required(redirect_field_name='/')
# def restart_test(request):
#     """Choice: results or restart test"""
#     if ResultOfTest.objects.filter(user=request.user).exists():
#         return render(request, 'rec_app/restart_test.html')
#     else:
#         return redirect(reverse('rec_app:start_test'))


#
# @login_required(redirect_field_name='/')
# def start_test(request):
#     """Start test"""
#     results = ResultOfTest.objects.filter(user=request.user)
#     if results.exists():
#         if results.count() < 10:
#             results.delete()
#             return redirect(reverse('rec_app:question_and_answers', args=(1,)))
#         else:
#             return redirect(reverse('rec_app:restart_test'))
#     return redirect(reverse('rec_app:question_and_answers', args=(1,)))
