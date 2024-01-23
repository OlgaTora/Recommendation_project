from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from catalog.filters import GroupsFilterSearch, GroupsFilterCatalog
from catalog.forms import SearchForm, DateTimeChoiceForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups


#
# class IndexView(View):
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['message'] = 'Поиск по каталогу занятий'
#         return context
#
#     def render(self, request):
#         return render(request, 'catalog/catalog.html', {'form': self.form})
#
#     def post(self, request):
#         self.form = SearchForm(request.POST)
#         if self.form.is_valid():
#             search_activity = self.form.cleaned_data['search_activity']
#             return redirect('post_list')
#         return self.render(request)
#
#     def get(self, request):
#         self.form = SearchForm()
#         return self.render(request)


def index(request):
    activity_types = ActivityTypes.objects.all().order_by('id')
    message = 'Поиск по каталогу занятий'
    form = SearchForm(request.POST or None)
    if form.is_valid():
        search_activity = form.cleaned_data['search_activity']
        return redirect(reverse('catalog:search', args=(search_activity,)))

    return render(
        request,
        'catalog/catalog.html',
        {'activity_types': activity_types,
         'form': form, 'message': message}
    )


def search(request, search_string: str):
    message = 'Результаты поиска:'
    level3 = ActivityLevel3.objects.filter(Q(descript_level__icontains=search_string) |
                                           Q(level__icontains=search_string))
    groups = Groups.objects.filter(level__in=level3).exclude(schedule_active='')
    group_filter = GroupsFilterSearch(request.GET, queryset=groups)
    groups = group_filter.qs

    paginator = Paginator(groups, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/search_results.html',
        {'groups': page_obj,
         'message': message,
         'group_filter': group_filter}
    )


def type_content(request, type_slug):
    message = 'Выберите раздел по вкусу:'
    activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
    level1 = ActivityLevel1.objects.filter(activity_type=activity_type).order_by('id')
    return render(
        request,
        'catalog/types.html',
        {
            'level1': level1,
            'message': message}
    )


def level1_content(request, type_slug, level1_slug):
    message = 'Выберите раздел по настроению'
    activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
    level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
    level2 = ActivityLevel2.objects.filter(activity_type=level1)
    return render(
        request,
        'catalog/level1.html',
        {'level2': level2,
         'message': message}
    )


def level2_content(request, type_slug, level1_slug, level2_slug):
    message = 'Выберите раздел по любви'
    activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
    level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
    level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
    level3 = ActivityLevel3.objects.filter(activity_type=level2)
    return render(
        request,
        'catalog/level2.html',
        {'level3': level3,
         'message': message}
    )


def level3_content(request, type_slug, level1_slug, level2_slug, level3_slug):
    activity_type = get_object_or_404(ActivityTypes, slug=type_slug)
    level1 = get_object_or_404(ActivityLevel1, slug=level1_slug)
    level2 = get_object_or_404(ActivityLevel2, slug=level2_slug)
    level3 = get_object_or_404(ActivityLevel3, slug=level3_slug)
    groups = Groups.objects.filter(level=level3).exclude(schedule_active='')

    groups_filter = GroupsFilterCatalog(request.GET, queryset=groups)
    groups = groups_filter.qs
    paginator = Paginator(groups, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/level3.html',
        {'groups': page_obj, 'groups_filter': groups_filter, 'level3': level3}
    )


@login_required
def signup2group(request, group: Groups):
    group = get_object_or_404(Groups, pk=group)
    user = request.user
    form = DateTimeChoiceForm(request.POST or None, group=group, user=user)
    if form.is_valid():
        form.save()
        return redirect(reverse('catalog:success_signup2group', args=(group.pk,)))
    return render(request, 'catalog/signup_group_details.html',
                  {'group': group, 'form': form})


#
# class Signup2GroupView(View):
#     def get_object(self, queryset=None):
#         group = get_object_or_404(Women.published, pk=self.kwargs[self.slug_url_kwarg])
#         return group
#
#     group = get_object_or_404(Groups, pk=group)
#     user = request.user
#     template_name = 'catalog/signup_group_details.html'
#     form_class = DateTimeChoiceForm
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, group=group, user=user)
#         if form.is_valid():
#             return redirect(reverse('catalog:success_signup2group', args=(group.pk,)))
#         else:
#             return render(request, self.template_name, {'form': form})


def success_signup2group(request, group: Groups):
    group = get_object_or_404(Groups, pk=group)
    return render(request, 'catalog/signup2group_result.html',
                  {'group': group})
