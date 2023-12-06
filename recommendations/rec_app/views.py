from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models.query import EmptyQuerySet
from django.forms import formset_factory, modelformset_factory, Textarea, ChoiceField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import http
from django.db.models import Q, Count
from django.urls import reverse
from django.views import generic

from address_book.models import StreetsBook
from catalog.models import Groups, ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3
from data_transform.street_types_dict import street_types_dict
from .forms import SignupForm, LoginForm, AnswerForm, BaseAnswerFormSet, AnswerForm1
from .models import Profile, Question, Choice, ResultOfTest, TestResultDescription


def index(request):
    return render(request, 'base.html')


def signup(request):
    if not request.user.is_authenticated:
        message = 'Заполните данные о себе, пожалуйста'
        if request.method == 'POST':
            form = SignupForm(request.POST, request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Profile.objects.create_user(
                    username=data['username'],
                    password=data['password'],
                    birth_date=data['birth_date'],
                    address=data['address'],
                    gender=data['gender'])
                user = authenticate(username=data['username'],
                                    password=data['password'])
                if user is not None:
                    login(request, user)
                return http.HttpResponseRedirect('')
        else:
            form = SignupForm()
        return render(
            request,
            'rec_app/login.html',
            {'form': form, 'message': message}
        )
    else:
        return HttpResponseRedirect('/')


def user_login(request):
    if not request.user.is_authenticated:
        message = 'Введите ваше имя и пароль'
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                profile = authenticate(username=username, password=password)
                if profile is not None:
                    login(request, profile)
                    return render(request, 'base.html')
        else:
            form = LoginForm()
        return render(
            request,
            'rec_app/login.html',
            {'form': form, 'user': request.user, 'message': message}
        )
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect('/')


@login_required(redirect_field_name='/')
def recommendations(request):
    result = ResultOfTest.get_results(request.user)
    # НАДО СДЕЛАТЬ ЧТОБ В ТАБЛИЦЫ БЫЛИ ДАННЫЕ а не тут иф елс писать
    if result < 16:
        description = TestResultDescription.descriptions.filter(pk=1).first()
        activity_type = ActivityTypes.types.filter(pk=1).first()
    elif 16 < result < 33:
        description = TestResultDescription.descriptions.filter(pk=2).first()
        activity_type = ActivityTypes.types.filter(pk=2).first()
    else:
        description = TestResultDescription.descriptions.filter(pk=3).first()
        activity_type = ActivityTypes.types.filter(pk=3).first()

    level1 = ActivityLevel1.levels.filter(activity_type=activity_type)
    level2 = ActivityLevel2.levels.filter(activity_type__in=[i.pk for i in level1])
    level3 = ActivityLevel3.levels.filter(activity_type__in=[i.pk for i in level2])

    # район по адресу пользователя
    user_address = address_transform(request.user.address)
    user_address = StreetsBook.streets.filter(street_name=user_address).first()
    district = user_address.district.admin_district.admin_district_name

    # группы по типу активности из теста и из района пользователя
    groups_list = Groups.groups.filter(level__in=[i.pk for i in level3], districts__contains=district)

    return render(request, 'rec_app/recommendations.html',
                  {'result': result,
                   'description': description,
                   'groups_list': groups_list})


@login_required(redirect_field_name='/')
def question_form(request, page_num=1):
    message = 'Для получения рекомендаций ответьте, пожалуйста, на все вопросы.'
    last_page = int(Question.questions.latest('pk').pk) + 1
    user = request.user

    if page_num == last_page:
        if len(ResultOfTest.results.filter(user=user).annotate(count=Count('user'))) >= last_page - 1:
            return redirect('rec_app:recommendations')
        else:
            return redirect(reverse('rec_app:question_and_answers', args=(1, )))

    if page_num > last_page:
        return render(request, '404.html')

    question = get_object_or_404(Question, pk=page_num)
    form = AnswerForm(request.POST or None, page_num=page_num, user=user)
    if form.is_valid():
        print(f'form valid {page_num}')
        form.save()
        message = 'Ответ принят'
    page_num += 1

    return render(request,
                  'rec_app/question_form.html',
                  {'form': form, 'page_num': page_num, 'pk': question.pk, 'message': message})


def address_transform(address):
    # если адрес - одно слово
    if len(address.split(',')) != 1:
        address = address.split(',')[1].strip()
        # если можно выделить улицу и дом
        if len(address.split()) != 1:
            tmp = address.split()
            for word in tmp:
                for key, value in street_types_dict.items():
                    if word in value:
                        street_type = key
                        tmp.remove(word)
                        address = (' '.join(tmp))
    address = address.title()
    return address


# def test_form(request):
#     """Psginator test not work"""
#     question_list = Question.questions.get_queryset().order_by('id')
#     paginator = Paginator(question_list, 1)
#     page = request.GET.get('page')
#     try:
#         questions = paginator.page(page)
#         page_num = 1
#         if request.method == 'POST':
#             print(f'{page=} method POST')
#             form = AnswerForm(request.POST, page_num=page_num)
#             if form.is_valid():
#                 return HttpResponse('ок')
#         else:
#             page_num = 1
#             print(f'{page=} method GET')
#             form = AnswerForm(page_num=page_num)
#
#         return render(request, 'rec_app/question_form.html', {'form': form, 'page': page})
#
#     except PageNotAnInteger:
#         questions = paginator.page(1)
#         if request.method == 'POST':
#             form = AnswerForm(request.POST, page_num=1)
#             if form.is_valid():
#                 return HttpResponse('ок')
#         else:
#             form = AnswerForm(page_num=1)
#
#         return render(request,
#                       'rec_app/test_form.html',
#                       {'page': page, 'form': form,
#                        'question': questions})
#     except EmptyPage:
#         questions = paginator.page(paginator.num_pages)
#


def test1_form(request):
    """test formset dont work question id cant recieve"""
    choices = []
    for choice in Choice.choices.all():
        choices.append((choice.votes, choice.choice_text))

    # AnswerFormSet = modelformset_factory(Choice, fields=['choice_text'], formset=BaseAnswerFormSet,
    #                                      widgets={'question_text': ChoiceField(choices=choices)})

    AnswerFormSet = formset_factory(AnswerForm1)
    # questions = Question.questions.all()
    # questions = Question.objects.get_queryset().order_by('id')
    # AnswerFormSet = formset_factory(AnswerForm1)
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            return HttpResponse('ok')
    else:
        formset = AnswerFormSet()
    return render(request, 'rec_app/test_form.html', {'formset': formset})


def test2(request):
    message = ''
    choices = Choice.choices.all()
    questions = Question.questions.all()
    paginator = Paginator(questions, 1)
    page = request.GET.get('page')
    print(page)
    if request.method == 'POST':
        try:
            questions = paginator.page(page)
            form = AnswerForm(request.POST, page_num=page)

        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        return render(request, 'rec_app/test_form.html', {'form': form, 'message': message})
    else:
        form = AnswerForm(page_num=page)

# WORKING CODE
# def test1(request):
#     choices = Choice.choices.all()
#     questions = Question.questions.all()
#     paginator = Paginator(questions, 1)
#     page = request.GET.get('page')
#     if request.method == 'POST':
#         form = AnswerForm(request.POST, page_num=page)
#     try:
#         questions = paginator.page(page)
#
#     except PageNotAnInteger:
#         questions = paginator.page(1)
#     except EmptyPage:
#         questions = paginator.page(paginator.num_pages)
#     return render(request, 'rec_app/test2.html', {'questions': questions, 'choices': choices, })

# if not page.has_next():
#    print('3')



# choice = int(form.cleaned_data['choice'])
            # answer = Choice.choices.filter(votes=choice).first()
            #
            # # else:
            # result = ResultOfTest(answer=answer, user=request.user, question=question)
            # result.save()


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
