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
    levels = ActivityLevel1.levels.filter(activity_type=activity_type).order_by('id')
    return render(
        request,
        'catalog/types.html',
        {'levels': levels}
    )


def level1_content(request, pk_type, pk_level):
    activity_type = get_object_or_404(ActivityLevel1, pk=pk_level, activity_type=pk_type)
    level = ActivityLevel2.levels.filter(activity_type=activity_type)
    return render(
        request,
        'catalog/level.html',
        {'level': level}
    )
