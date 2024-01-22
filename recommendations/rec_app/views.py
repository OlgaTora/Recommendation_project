from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse

from address_book.models import StreetsBook
from catalog.filters import GroupsFilterSearch
from catalog.models import Groups, ActivityTypes, Attends
from .forms import AnswerForm
from .models import Question, ResultOfTest, TestResultDescription, VotesGroups
from django.contrib import messages


@login_required(redirect_field_name='/')
def recommendations(request):
    """Recommendation based on test results and user address, priority - offline"""
    global groups_list
    result = ResultOfTest.get_results(request.user)
    votes_group = VotesGroups.objects.get(votes=result)
    description = TestResultDescription.objects.get(pk=votes_group.result_group.pk)
    activity_type = ActivityTypes.objects.get(pk=description.activity_type.pk)

    # отфильтровать группы offline/online отдельно
    level3_offline, level3_online = Attends.get_top_level3()
    level3_offline = level3_offline.filter(activity_type__activity_type__activity_type=activity_type)
    level3_online = level3_online.filter(activity_type__activity_type__activity_type=activity_type)

    # адрес пользователя
    # так как нет инфо по району пользователя, берем все улицы с таким названием
    user_address = StreetsBook.address_transform(request.user.address)
    user_address = list(user_address)
    # если адрес есть в базе адресов Москвы
    if user_address:
        admin_districts = [i.admin_district.admin_district_name for i in user_address]
        # группы по типу активности из теста и из района пользователя
        for district in admin_districts:
            groups_list = (Groups.objects.filter(
                level__in=level3_offline,
                districts__icontains=district)
                .exclude(
                schedule_active=''))
            print('every district list')
            print(groups_list)
            # не работает такое соединение выборок!!!
            groups_list.union(groups_list)
        # ТУТ НЕВЕРНО СДЕЛАНО. почему-то фильтр не выбирает результаты он лайн
        groups_list_on = Groups.objects.filter(level__in=level3_online).exclude(schedule_active='')
        print('every online list')
        print(groups_list_on)
        groups_list_on.union(groups_list)
        print('every union list')
        print(groups_list)
    else:
        groups_list = (Groups.objects.filter(level__in=level3_online)
                       .exclude(schedule_active=''))

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
    #page_num += 1
    return render(request,
                  'rec_app/test_form.html',
                  {'form': form, 'pk': question.pk, 'message': message})


@login_required(redirect_field_name='/')
def start_test(request):
    """Start test"""
    if ResultOfTest.objects.filter(user=request.user).exists():
        if ResultOfTest.objects.filter(user=request.user).count() < 10:
            ResultOfTest.objects.filter(user=request.user).delete()
            return redirect(reverse('rec_app:question_and_answers', args=(1,)))
        else:
            return redirect(reverse('rec_app:restart_test'))
    return redirect(reverse('rec_app:question_and_answers', args=(1,)))


@login_required(redirect_field_name='/')
def restart_test(request):
    """Choice: results or restart test"""
    if ResultOfTest.objects.filter(user=request.user).exists():
        return render(request, 'rec_app/restart_test.html')
    else:
        return redirect(reverse('rec_app:start_test'))
