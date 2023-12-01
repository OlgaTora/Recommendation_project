from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django import http
from django.db.models import Q
from address_book.models import District, StreetsBook
from catalog.models import Groups, ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3
from data_transform.street_types_dict import street_types_dict
from .forms import SignupForm, LoginForm, AnswerForm, AnswerForm1
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


# а если человек уже проходил тест?
def question_form(request, page_num=1):
    message = None
    last_question = Question.questions.latest('pk')
    if page_num == int(last_question.pk) + 1:
        return HttpResponseRedirect('/recommendations/')
    question = get_object_or_404(Question, pk=page_num)
    if request.method == 'POST':
        form = AnswerForm(request.POST, page_num=page_num)
        if form.is_valid():
            """Надо сделать чтоб нельзя было вернуться назад и поменять ответ,
            а также чтоб попадать  только на 1ый вопрос
            """
            choice = int(form.cleaned_data['choice'])
            answer = Choice.choices.filter(votes=choice).first()
            # answer = Choice.choices.filter(question=question, votes=choice).first()
            result = ResultOfTest(answer=answer, user=request.user, question=question)
            result.save()
            message = 'Ответ принят'
    else:
        form = AnswerForm(page_num=page_num)
    page_num += 1

    return render(request,
                  'rec_app/question_form.html',
                  {'form': form, 'page_num': page_num, 'pk': question.pk, 'message': message})


def address_transform(address):
    address = address.split(',')[1].strip()
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
#
# def test1_form(request):
#     questions = Question.questions.filter(pk__lt=5)
#     """ choice last"""
#     if request.method == 'POST':
#         form = AnswerForm(request.POST, questions)
#         if form.is_valid():
#             return HttpResponse('ок')
#     else:
#         form = AnswerForm(questions)
#     return render(request, 'rec_app/test_form.html', {'form': form, 'questions': questions})
#

def test1_form(request):
    """test formset dont work question id cant recieve"""
    AnswerFormSet = modelformset_factory(Question, fields=['question_text'])
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
