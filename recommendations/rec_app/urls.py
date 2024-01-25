from django.urls import path
from . import views

app_name = 'rec_app'

urlpatterns = [
    path('', views.StartView.as_view(), name='start_test'),
    path('restart/', views.RestartView.as_view(), name='restart_test'),
    path('<int:page_num>/', views.question_form, name='question_and_answers'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
