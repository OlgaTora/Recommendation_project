from django.urls import path
from . import views

app_name = 'rec_app'

urlpatterns = [
    path('', views.start_test, name='start_test'),
    path('restart/', views.restart_test, name='restart_test'),
    path('<int:page_num>/', views.question_form, name='question_and_answers'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
