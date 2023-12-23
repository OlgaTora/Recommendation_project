from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.urls import reverse

from address_book.models import StreetsBook
from catalog.models import Groups, ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Attends
from .forms import AnswerForm
from .models import Question, ResultOfTest, TestResultDescription
from django.contrib import messages


@login_required(redirect_field_name='/')
def recommendations(request):
    result = ResultOfTest.get_results(request.user)
    # НАДО СДЕЛАТЬ ЧТОБ В ТАБЛИЦЫ БЫЛИ ДАННЫЕ а не тут иф елс писать
    if result < 16:
        description = TestResultDescription.descriptions.get(pk=1)
        activity_type = ActivityTypes.types.get(pk=1)
    elif 16 < result < 33:
        description = TestResultDescription.descriptions.get(pk=2)
        activity_type = ActivityTypes.types.get(pk=2)
    else:
        description = TestResultDescription.descriptions.get(pk=3)
        activity_type = ActivityTypes.types.get(pk=3)

    level1 = ActivityLevel1.levels.filter(activity_type=activity_type)
    level2 = ActivityLevel2.levels.filter(activity_type__in=[i.pk for i in level1])
    level3_top = Attends.get_top_level3().filter(activity_type__in=[i.pk for i in level2])
    level3_online = level3_top.filter(level__contains='ОНЛАЙН')

    # район по адресу пользователя
    user_address = StreetsBook.address_transform(request.user.address)
    user_address = user_address.first()
    # если адрес есть в базе адресов Москвы
    if user_address:
        district = user_address.district.admin_district.admin_district_name
        # группы по типу активности из теста и из района пользователя
        groups_list = (Groups.groups.filter(level__in=[i.pk for i in level3_top]) & Groups.groups.filter(
            Q(districts__contains=district) | Q(level__in=[i.pk for i in level3_online]))
                       .order_by('uniq_id'))
    else:
        groups_list = (Groups.groups.filter(level__in=[i.pk for i in level3_top])
                       .order_by('uniq_id'))

    # сделать высплывающее окно с районом? есть улицы с одинаковым названием
    # в левел3 должны быть топ активностей для данного юзера
    # if len(list(user_address)) == 1:
    #     user_address = user_address.first()
    #     district = user_address.district.admin_district.admin_district_name
    # else:
    #     return redirect('users:district_choice')

    paginator = Paginator(groups_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'rec_app/recommendations.html',
                  {'result': result,
                   'description': description,
                   'groups_list': page_obj})


@login_required(redirect_field_name='/')
def question_form(request, page_num=1):
    if ResultOfTest.results.filter(user=request.user).exists():
        if ResultOfTest.results.filter(user=request.user).count() == 10:
            # messages.error(request, 'Вы уже отвечали на вопросы теста.')
            return redirect('rec_app:recommendations')

    message = 'Для получения рекомендаций ответьте, пожалуйста, на все вопросы.'
    last_page = int(Question.questions.latest('pk').pk) + 1
    user = request.user
    if page_num > last_page:
        return render(request, '404.html')

    if page_num == last_page:
        if len(ResultOfTest.results.filter(user=user).annotate(count=Count('user'))) == last_page - 1:
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
    page_num += 1
    return render(request,
                  'rec_app/test_form.html',
                  {'form': form, 'pk': question.pk, 'message': message})


@login_required(redirect_field_name='/')
def start_test(request):
    if ResultOfTest.results.filter(user=request.user).exists():
        if ResultOfTest.results.filter(user=request.user).count() < 10:
            ResultOfTest.results.filter(user=request.user).delete()
    return redirect(reverse('rec_app:question_and_answers', args=(1,)))


# а  если 1-Я
# user_address = request.user.address.split(',')[1].strip()
# if len(user_address.split()) == 1:
#     user_address = user_address.title()
# else:
#     tmp = user_address.split()
#     for word in tmp:
#         for key, value in street_types_dict.items():
#             if word in value:
#                 street_type = key
#                 tmp.remove(word)
#                 user_address = (' '.join(tmp)).title()
