from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.urls import reverse

from address_book.models import StreetsBook
from catalog.models import Groups, ActivityTypes, Attends
from .forms import AnswerForm
from .models import Question, ResultOfTest, TestResultDescription, VotesGroups
from django.contrib import messages


@login_required(redirect_field_name='/')
def recommendations(request):
    result = ResultOfTest.get_results(request.user)
    votes_group = VotesGroups.votes_groups.get(votes=result)
    description = TestResultDescription.descriptions.get(pk=votes_group.result_group.pk)
    activity_type = ActivityTypes.types.get(pk=description.activity_type.pk)
    level3_top = Attends.get_top_level3().filter(activity_type__activity_type__activity_type=activity_type)

    # отфильтровать группы offline/online отдельно
    level3_offline = level3_top.exclude(level__icontains='ОНЛАЙН')[:3]
    level3_online = level3_top.filter(level__icontains='ОНЛАЙН')[:3]

    # район по адресу пользователя
    user_address = StreetsBook.address_transform(request.user.address)
    # так как нет инфо по району пользователя, берем все улицы с таким названием
    user_address = list(user_address)

    # если адрес есть в базе адресов Москвы
    if user_address:
        admin_district = [i.admin_district.admin_district_name for i in user_address]

        # группы по типу активности из теста и из района пользователя
        groups_list = (Groups.groups.filter
                       (Q(level__in=[i.pk for i in level3_offline], districts__in=[admin_district]) |
                        Q(level__in=[i.pk for i in level3_online])
                        )
                       .exclude(schedule_active=''))
    else:
        groups_list = (Groups.groups.filter(level__in=[i.pk for i in level3_top])
                       .exclude(schedule_active=''))

    # сделать высплывающее окно с районом? есть улицы с одинаковым названием
    # в левел3 должны быть топ активностей для данного юзера
    # if len(list(user_address)) == 1:
    #     user_address = user_address.first()
    #     district = user_address.district.admin_district.admin_district_name
    # else:
    #     return redirect('users:district_choice')

    paginator = Paginator(groups_list, 5)
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
        else:
            return redirect(reverse('rec_app:restart_test'))
    return redirect(reverse('rec_app:question_and_answers', args=(1,)))


@login_required(redirect_field_name='/')
def restart_test(request):
    if ResultOfTest.results.filter(user=request.user).exists():
        return render(request, 'rec_app/restart_test.html')


#
# class DeleteObject(LoginRequiredMixin, DeleteView):
#     model = Object
#     template_name = 'todoList/home.html'
#
#     def get(self, request, *args, **kwargs):
#         obj = get_object_or_404(Object, id=self.kwargs.get('id'))
#         # Check for uncompleted tasks
#         uncompleted = Data.objects.filter(objects=obj).filter(state=False).count()
#
#         if uncompleted == 0:
#             obj.delete()
#         return redirect('home')

"""
<a class="dropdown-item" data-toggle="modal" data-target="#taskModal" onclick="getUrl('{% url 'del_obj' object.id %}')">Delete</a>

<script language="javascript">
    function getUrl(url) {
        del_obj.setAttribute('href', url);
    }
    function goto() {
        var url = del_obj.getAttribute('href');
        return location.href = url;
    }
</script>

<div id="taskModal" class="modal fade">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title">Confirm deletion</h4>
            </div>
            <div class="modal-body">Are your sure you want to delete?</div>
            <div class="modal-footer">
                <a id="del_obj" class="btn btn-danger" type="button" data-dismiss="modal" href="" onclick="goto()">Delete</a>
                <a class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</a>
            </div>
        </div>
    </div>
</div>
"""
