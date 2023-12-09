from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from catalog.forms import SearchForm
from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3, Groups


def index(request):
    activity_types = ActivityTypes.types.all().order_by('id')
    return render(
        request,
        'catalog/catalog.html',
        {'activity_types': activity_types}
    )


def search(request):
    """ название офп ищется но косяк в открытии левел2"""
    message = 'Поиск по каталогу занятий'
    form = SearchForm(request.POST or None)
    if form.is_valid():
        message = 'Поиск по каталогу занятий'
        search_activity = form.cleaned_data['search_activity']
        level3 = ActivityLevel3.levels.filter(level__contains=search_activity)
        # level3_names = level3.level
        level2 = ActivityLevel2.levels.get(level=level3.first().activity_type)
        level1 = ActivityLevel1.levels.get(level=level2.activity_type)
        activity_type = ActivityTypes.types.get(activity_type=level1.activity_type)
        return render(
            request,
            'catalog/level2.html',
            {'level1': level1,
             'level2': level2,
             'level3': level3,
             'activity_type': activity_type, })
    return render(request, 'catalog/search.html', {'form': form, 'message': message})


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
    activity_type = get_object_or_404(ActivityTypes, pk=pk_type)
    level1 = get_object_or_404(ActivityLevel1, pk=pk_level1)
    level2 = get_object_or_404(ActivityLevel2, pk=pk_level2)
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
