from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django import http

from .forms import SignupForm, LoginForm, AnswerForm
from .models import Profile, Question, Choice, ResultOfTest


def index(request):
    return render(request, 'base.html')


def catalog(request):
    return render(request, 'rec_app/catalog.html')


def search(request):
    return render(request, 'rec_app/search.html')


def signup(request):
    message = 'Fill this form to sign up'
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


def user_login(request):
    message = 'Please, input username and password'
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile = authenticate(username=username, password=password)
            if profile is not None:
                login(request, profile)
                # return HttpResponseRedirect('/')
                return render(request, 'base.html')
    else:
        form = LoginForm()
    return render(
        request,
        'rec_app/login.html',
        {'form': form, 'user': request.user, 'message': message}
    )


def user_logout(request):
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect('/')


def question_form(request, page_num=1):
    last_question = Question.objects.latest('pk')
    if page_num == int(last_question.pk) + 1:
        return HttpResponseRedirect('/catalog/')
    question = get_object_or_404(Question, pk=page_num)
    if request.method == 'POST':
        form = AnswerForm(request.POST, page_num=page_num)
        if form.is_valid():
            print(question)
            """Надо переделать поиск ответа и чтобы вопрос был текущий а не плюс 1
            также чтоб нельзя было вернуться назад и поменять ответ,
            а также чтоб попадать сразу только на 1ый вопрос
            """
            choice = int(form.cleaned_data['choice'])
            answers = Choice.objects.filter(question=question)
            for answer in answers:
                if answer.votes == choice:
                    user = request.user
                    result = ResultOfTest(answer=answer, user=user, question=question)
                    result.save()
    else:
        form = AnswerForm(page_num=page_num)
    page_num += 1

    return render(request,
                  'rec_app/question_form.html',
                  {'form': form, 'page_num': page_num, 'pk': question.pk})


def test_form(request):
    """Psginator test not work"""
    question_list = Question.objects.get_queryset().order_by('id')
    paginator = Paginator(question_list, 1)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
        page_num = 1
        if request.method == 'POST':
            print(f'{page=} method POST')
            form = AnswerForm(request.POST, page_num=page_num)
            if form.is_valid():
                return HttpResponse('ок')
        else:
            page_num = 1
            print(f'{page=} method GET')
            form = AnswerForm(page_num=page_num)

        return render(request, 'rec_app/question_form.html', {'form': form, 'page': page})

    except PageNotAnInteger:
        questions = paginator.page(1)
        if request.method == 'POST':
            form = AnswerForm(request.POST, page_num=1)
            if form.is_valid():
                return HttpResponse('ок')
        else:
            form = AnswerForm(page_num=1)

        return render(request,
                      'rec_app/test_form.html',
                      {'page': page, 'form': form,
                       'question': questions})
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)


def test1_form(request):
    questions = Question.objects.filter(pk__lt=5)
    """ choice last"""
    if request.method == 'POST':
        form = AnswerForm(request.POST, questions)
        if form.is_valid():
            return HttpResponse('ок')
    else:
        form = AnswerForm(questions)
    return render(request, 'rec_app/test_form.html', {'form': form, 'questions': questions})


def tes1t_form(request):
    """test formset dont work question id cant recieve"""
    questions = Question.objects.filter(pk__lt=5)
    # questions = Question.objects.get_queryset().order_by('id')
    AnswerFormSet = formset_factory(AnswerForm)
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            return HttpResponse('ok')
    else:
        formset = AnswerFormSet()
    return render(request, 'rec_app/test_form.html', {'formset': formset, 'questions': questions})
