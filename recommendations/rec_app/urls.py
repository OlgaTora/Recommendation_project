from django.urls import path
from . import views

app_name = 'rec_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('catalog/', views.catalog, name='catalog'),
    # path('search/', views.search, name='search'),
    # path('test/', views.question_form, name='question_and_answers'),
    path('test/<int:page_num>/', views.question_form, name='question_and_answers'),
    path('recommendations/', views.recommendations, name='recommendations'),
]