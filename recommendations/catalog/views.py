from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from catalog.filters import GroupsFilterSearch, GroupsFilterCatalog
from catalog.forms import SearchForm, DateTimeChoiceForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups, Attends


class IndexView(FormView):
    template_name = 'catalog/catalog.html'
    extra_context = {'message': 'Поиск по каталогу занятий'}
    form_class = SearchForm
    context_object_name = 'activity_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity_types = ActivityTypes.objects.all().order_by('id')
        context['activity_types'] = activity_types
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            search_activity = form.cleaned_data['search_activity']
            return redirect(reverse('catalog:search', args=(search_activity,)))


class SearchView(FilterView):
    model = Groups
    paginate_by = 25
    template_name = 'catalog/search_results.html'
    context_object_name = 'groups'
    filterset_class = GroupsFilterSearch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Результаты поиска'
        return context

    def get_queryset(self):
        search_string = self.kwargs['search_string']
        level3 = ActivityLevel3.objects.filter(Q(descript_level__icontains=search_string) |
                                               Q(level__icontains=search_string))
        groups = Groups.objects.filter(level__in=level3).exclude(schedule_active='')
        return groups


class TypeView(ListView):
    model = ActivityLevel1
    template_name = 'catalog/catalog_levels_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Выберите раздел по вкусу:'
        context['next_page'] = 'level1/'
        return context

    def get_queryset(self):
        type_slug = self.kwargs['type_slug']
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
        level1_slug = self.kwargs['level1_slug']
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
        level2_slug = self.kwargs['level2_slug']
        level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
        level3 = ActivityLevel3.objects.filter(activity_type=level2)
        return level3


class Level3View(FilterView):
    model = Groups
    paginate_by = 25
    template_name = 'catalog/groups.html'
    context_object_name = 'groups'
    filterset_class = GroupsFilterCatalog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level3_slug = self.kwargs['level3_slug']
        context['level3'] = get_object_or_404(ActivityLevel3, slug=level3_slug)
        return context

    def get_queryset(self):
        level3_slug = self.kwargs['level3_slug']
        level3 = get_object_or_404(ActivityLevel3, slug=level3_slug)
        groups = Groups.objects.filter(level=level3).exclude(schedule_active='')
        return groups


class SignUp2GroupView(FormView, LoginRequiredMixin):
    template_name = 'catalog/signup2group.html'
    extra_context = {'message': 'Выберите время и дату посещения'}
    form_class = DateTimeChoiceForm
    context_object_name = 'group'
    redirect_field_name = reverse_lazy('users:index')

    def get_success_url(self):
        attend = Attends.objects.latest('id')
        return reverse_lazy('catalog:group_success_signup', args=(attend.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_pk = self.kwargs['group']
        context['group'] = get_object_or_404(Groups, pk=group_pk)
        return context

    def form_valid(self, form):
        form.save()
        return super(SignUp2GroupView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(SignUp2GroupView, self).get_form_kwargs()
        kwargs['group'] = get_object_or_404(Groups, pk=self.kwargs.get('group'))
        kwargs['user'] = self.request.user
        return kwargs


class SuccessSignup(LoginRequiredMixin, DetailView):
    model = Groups
    context_object_name = 'attend'
    template_name = 'catalog/group_success_signup.html'
    extra_context = {'message': 'Вы успешно записались!'}
    redirect_field_name = reverse_lazy('users:index')

    def get_object(self, queryset=None):
        slug = self.kwargs['pk']
        return get_object_or_404(Attends, pk=slug)

# def search(request, search_string: str):
#     message = 'Результаты поиска:'
#     level3 = ActivityLevel3.objects.filter(Q(descript_level__icontains=search_string) |
#                                            Q(level__icontains=search_string))
#     groups = Groups.objects.filter(level__in=level3).exclude(schedule_active='')
#     group_filter = GroupsFilterSearch(request.GET, queryset=groups)
#     groups = group_filter.qs
#
#     paginator = Paginator(groups, 25)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(
#         request,
#         'catalog/search_results.html',
#         {'groups': page_obj,
#          'message': message,
#          'group_filter': group_filter}
#     )

#
# def type_content(request, type_slug):
#     message = 'Выберите раздел по вкусу:'
#     activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
#     level1 = ActivityLevel1.objects.filter(activity_type=activity_type).order_by('id')
#     return render(
#         request,
#         'catalog/types.html',
#         {
#             'level1': level1,
#             'message': message}
#     )
#
#
# def level1_content(request, type_slug, level1_slug):
#     message = 'Выберите раздел по настроению'
#     activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
#     level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
#     level2 = ActivityLevel2.objects.filter(activity_type=level1)
#     return render(
#         request,
#         'catalog/level1.html',
#         {'level2': level2,
#          'message': message}
#     )
#
#
# def level2_content(request, type_slug, level1_slug, level2_slug):
#     message = 'Выберите раздел по любви'
#     activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
#     level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
#     level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
#     level3 = ActivityLevel3.objects.filter(activity_type=level2)
#     return render(
#         request,
#         'catalog/level2.html',
#         {'level3': level3,
#          'message': message}
#     )
#
#
# def level3_content(request, type_slug, level1_slug, level2_slug, level3_slug):
#     activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
#     level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
#     level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
#     level3 = get_object_or_404(ActivityLevel3, slug=level3_slug)
#     groups = Groups.objects.filter(level=level3).exclude(schedule_active='')
#
#     groups_filter = GroupsFilterCatalog(request.GET, queryset=groups)
#     groups = groups_filter.qs
#     paginator = Paginator(groups, 25)
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(
#         request,
#         'catalog/level3.html',
#         {'groups': page_obj, 'groups_filter': groups_filter, 'level3': level3}
#     )

#
# @login_required
# def signup2group(request, group: Groups):
#     message = 'Выберите время и дату посещения'
#     group = get_object_or_404(Groups, pk=group)
#     user = request.user
#     form = DateTimeChoiceForm(request.POST or None, group=group, user=user)
#     if form.is_valid():
#         form.save()
#         attend = Attends.objects.latest('id')
#         return redirect(reverse('catalog:group_success_signup', args=(attend.pk,)))
#     return render(request, 'catalog/signup2group.html',
#                   {'group': group, 'message': message, 'form': form})

#
# def index(request):
#     activity_types = ActivityTypes.objects.all().order_by('id')
#     message = 'Поиск по каталогу занятий'
#     form = SearchForm(request.POST or None)
#     if form.is_valid():
#         search_activity = form.cleaned_data['search_activity']
#         return redirect(reverse('catalog:search', args=(search_activity,)))
#
#     return render(
#         request,
#         'catalog/catalog.html',
#         {'activity_types': activity_types,
#          'form': form, 'message': message}
#     )
