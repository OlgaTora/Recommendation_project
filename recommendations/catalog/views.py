from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from catalog.filters import GroupsFilterSearch, GroupsFilterCatalog
from catalog.forms import SearchForm, DateTimeChoiceForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups


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
        {'activity_types': activity_types, 'form': form, 'message': message}
    )


def search(request, search_string: str):
    message = 'Результаты поиска:'
    level3 = ActivityLevel3.objects.filter(Q(descript_level__icontains=search_string) |
                                           Q(level__icontains=search_string))
    groups = Groups.objects.filter(level__in=list(level3)).exclude(schedule_active='')
    myFilter = GroupsFilterSearch(request.GET, queryset=groups)
    groups = myFilter.qs

    paginator = Paginator(groups, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/search_results.html',
        {'groups': page_obj, 'message': message, 'myFilter': myFilter}
    )


def type_content(request, pk_type):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = ActivityLevel1.objects.filter(activity_type=activity_type).order_by('id')
    return render(
        request,
        'catalog/types.html',
        {'level1': level1, 'activity_type': activity_type}
    )


def level1_content(request, pk_type, pk_level1):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    level2 = ActivityLevel2.objects.filter(activity_type=level1)
    return render(
        request,
        'catalog/level1.html',
        {'level1': level1, 'level2': level2, 'activity_type': activity_type}
    )


def level2_content(request, pk_type, pk_level1, pk_level2):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    level2 = get_object_or_404(ActivityLevel2, pk=pk_level2)
    level3 = ActivityLevel3.objects.filter(activity_type=level2)
    return render(
        request,
        'catalog/level2.html',
        {'level1': level1,
         'level2': level2,
         'level3': level3,
         'activity_type': activity_type, })


def level3_content(request, pk_type, pk_level1, pk_level2, pk_level3):
    # activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    # level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    # level2 = get_object_or_404(ActivityLevel2, pk=pk_level2)
    level3 = get_object_or_404(ActivityLevel3, pk=pk_level3)
    groups = Groups.objects.filter(level=level3).exclude(schedule_active='')

    myFilter = GroupsFilterCatalog(request.GET, queryset=groups)
    groups = myFilter.qs
    paginator = Paginator(groups, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/level3.html',
        {'groups': page_obj, 'myFilter': myFilter, 'level3': level3}
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


def success_signup2group(request, group: Groups):
    group = get_object_or_404(Groups, pk=group)
    return render(request, 'catalog/signup2group_result.html',
                  {'group': group})
