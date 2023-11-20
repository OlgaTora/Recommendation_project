from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='catalog'),
    # path('<int:pk_type>/', views.type_content, name='type_content'),
    re_path(r"^(?:types-(?P<pk_type>[0-9]+)/)?$", views.type_content, name='type_content'),
    re_path(r"^(?:types-(?P<pk_type>[0-9]+)&level1-(?P<pk_level1>[0-9]+)/)?$", views.level1_content,
            name='level1_content'),

    # path('<int:pk_type>/<int:pk_level>/', views.level_content, name='level_content'),
    path('search/', views.search, name='search'),
]
