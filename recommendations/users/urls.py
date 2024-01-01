from django.urls import path, re_path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # re_path(r'^street-autocomplete/$', views.StreetAutocomplete.as_view(), name='street-autocomplete'),
]

