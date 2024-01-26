from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogOutView.as_view(), name='logout'),
]

