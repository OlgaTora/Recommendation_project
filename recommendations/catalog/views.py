from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from catalog.forms import SearchForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups


def index(request):
    activity_types = ActivityTypes.types.all().order_by('id')
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
    level3 = list(ActivityLevel3.levels.filter(level__icontains=search_string))
    groups = Groups.groups.filter(level__in=level3).exclude(schedule_active='')
    paginator = Paginator(groups, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/search_results.html',
        {'groups': page_obj, 'message': message}
    )


def type_content(request, pk_type):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = ActivityLevel1.levels.filter(activity_type=activity_type).order_by('id')
    return render(
        request,
        'catalog/types.html',
        {'level1': level1, 'activity_type': activity_type}
    )


def level1_content(request, pk_type, pk_level1):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    level2 = ActivityLevel2.levels.filter(activity_type=level1)
    return render(
        request,
        'catalog/level1.html',
        {'level1': level1, 'level2': level2, 'activity_type': activity_type}
    )


def level2_content(request, pk_type, pk_level1, pk_level2):
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    level2 = get_object_or_404(ActivityLevel2, pk=pk_level2)
    level3 = ActivityLevel3.levels.filter(activity_type=level2)
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
    groups = Groups.groups.filter(level=level3).exclude(schedule_active='')
    paginator = Paginator(groups, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/level3.html',
        {'level3': level3,
         'groups': page_obj}
    )


@login_required
def signup2group(request, group: Groups):
    group = get_object_or_404(Groups, pk=group)

    # group = Groups.groups.get(id=group)
    # Attends.attends.create(
    #     uniq_id=id,
    #     group_id=group.uniq_id,
    #     user_id=request.user.pk,
    #     online='',
    #     date_attend,
    #     start_time,
    #     end_time
    # )
    return render(request, 'catalog/signup2group_result.html', {'group': group})
