from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='catalog'),
    re_path(r"^(?P<pk_type>[0-9]+)/$", views.type_content, name='type_content'),
    re_path(r"^(?P<pk_type>[0-9]+)/(?P<pk_level1>[0-9]+)/$", views.level1_content,
            name='level1_content'),
    re_path(r"^(?P<pk_type>[0-9]+)/(?P<pk_level1>[0-9]+)/(?P<pk_level2>[0-9]+)$", views.level2_content,
            name='level2_content'),
    re_path(r"^(?P<pk_type>[0-9]+)/(?P<pk_level1>[0-9]+)/(?P<pk_level2>[0-9]+)/(?P<pk_level3>[0-9]+)$",
            views.level3_content, name='level3_content'),
    path('search/<str:search_string>', views.search, name='search'),
]
