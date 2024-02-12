from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django_filters.views import FilterView

from catalog.filters import GroupsFilterSearch, GroupsFilterCatalog
from catalog.forms import SearchForm, DateTimeChoiceForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups, Attends, \
    GroupsCorrect


class IndexView(FormView):
    template_name = 'catalog/catalog.html'
    extra_context = {
        'message': 'Каталог занятий',
        'searcher': 'Введите слово для поиска по каталогу'
    }
    form_class = SearchForm
    context_object_name = 'activity_types'

    def get_success_url(self, search_activity=None):
        return reverse_lazy('catalog:search', args=(search_activity,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_types'] = ActivityTypes.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        search_activity = form.cleaned_data.get('search_activity')
        return redirect(self.get_success_url(search_activity))


class SearchView(FilterView):
    model = GroupsCorrect
    paginate_by = 10
    template_name = 'catalog/search_results.html'
    extra_context = {'message': 'Результаты поиска'}
    context_object_name = 'groups_list'
    filterset_class = GroupsFilterSearch

    def get_queryset(self):
        search_string = self.kwargs.get('search_string')
        level3 = ActivityLevel3.objects.filter(Q(descript_level__icontains=search_string) |
                                               Q(level__icontains=search_string))
        groups_list = GroupsCorrect.objects.filter(level__in=level3).exclude(start_date='')
        return groups_list


class TypeView(ListView):
    model = ActivityLevel1
    template_name = 'catalog/catalog_levels_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Выберите раздел по вкусу:'
        context['next_page'] = 'level1/'
        return context

    def get_queryset(self):
        type_slug = self.kwargs.get('type_slug')
        activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
        level1 = ActivityLevel1.objects.filter(activity_type=activity_type).order_by('id')
        return level1


class Level1View(ListView):
    model = ActivityLevel2
    template_name = 'catalog/catalog_levels_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Выберите раздел по настроению:'
        context['next_page'] = 'level2/'
        return context

    def get_queryset(self):
        level1_slug = self.kwargs.get('level1_slug')
        level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
        level2 = ActivityLevel2.objects.filter(activity_type=level1)
        return level2


class Level2View(ListView):
    model = ActivityLevel3
    template_name = 'catalog/catalog_levels_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Выберите раздел по любви:'
        context['next_page'] = 'level3/'
        return context

    def get_queryset(self):
        level2_slug = self.kwargs.get('level2_slug')
        level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
        level3 = ActivityLevel3.objects.filter(activity_type=level2)
        return level3


class Level3View(FilterView):
    model = GroupsCorrect
    paginate_by = 10
    template_name = 'catalog/groups.html'
    context_object_name = 'groups_list'
    extra_context = {'message': 'Выберите удобную для Вас группу'}
    filterset_class = GroupsFilterCatalog
    level3_slug: int

    def get_slug(self):
        if not hasattr(self, 'level3_slug'):
            self.level3_slug = self.kwargs.get('level3_slug')
        return self.level3_slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['level3'] = get_object_or_404(ActivityLevel3, slug=self.get_slug())
        return context

    def get_queryset(self):
        level3 = get_object_or_404(ActivityLevel3, slug=self.get_slug())
        groups_list = GroupsCorrect.objects.filter(level=level3).exclude(start_date='')
        return groups_list


class SignUp2GroupView(LoginRequiredMixin, FormView):
    template_name = 'catalog/signup2group.html'
    extra_context = {'message': 'Выберите дату посещения'}
    form_class = DateTimeChoiceForm
    context_object_name = 'group'
    redirect_field_name = 'users:index'
    group: GroupsCorrect

    def get_group(self):
        if not hasattr(self, 'group'):
            self.group = get_object_or_404(GroupsCorrect, pk=self.kwargs['group'])
        return self.group

    def get_success_url(self, date_choice=None):
        date_choice = Attends.objects.latest('id').date_attend
        return reverse_lazy('catalog:group_success_signup', args=(self.get_group().pk, date_choice))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.get_group()
        return context

    def form_valid(self, form):
        form.save()
        date_choice = form.cleaned_data.get('date_choice')
        return redirect(self.get_success_url(date_choice))

    def get_form_kwargs(self):
        kwargs = super(SignUp2GroupView, self).get_form_kwargs()
        kwargs['group'] = self.get_group()
        kwargs['user'] = self.request.user
        return kwargs


class SuccessSignup(LoginRequiredMixin, DetailView):
    model = GroupsCorrect
    context_object_name = 'group'
    template_name = 'catalog/group_success_signup.html'
    extra_context = {'message': 'Вы успешно записались!'}
    redirect_field_name = reverse_lazy('users:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_choice'] = self.kwargs['date_choice']
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(GroupsCorrect, pk=self.kwargs['pk'])
