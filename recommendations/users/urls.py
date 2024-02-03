from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

