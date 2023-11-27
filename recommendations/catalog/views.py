from django.shortcuts import render, get_object_or_404

from catalog.models import ActivityTypes, ActivityLevel1, ActivityLevel2, ActivityLevel3


def index(request):
    activity_types = ActivityTypes.types.all().order_by('id')
    return render(
        request,
        'catalog/catalog.html',
        {'activity_types': activity_types}
    )


def search(request):
    return render(request, 'catalog/search.html')


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
        {'level1': level1, 'level2': level2, 'level3': level3, 'activity_type': activity_type}
    )