from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='catalog'),
    path('types/<slug:type_slug>/', views.TypeView.as_view(), name='types'),
    path('types/<slug:type_slug>/level1/<slug:level1_slug>/', views.Level1View.as_view(), name='level1'),
    path('types/<slug:type_slug>/level1/<slug:level1_slug>/level2/<slug:level2_slug>/',
         views.Level2View.as_view(), name='level2'),
    path('types/<slug:type_slug>/level1/<slug:level1_slug>/level2/<slug:level2_slug>/level3/<slug:level3_slug>/',
         views.Level3View.as_view(), name='level3'),
    path('search/<str:search_string>', views.SearchView.as_view(), name='search'),
    path('signup2group/<str:group>', views.signup2group, name='signup2group'),
    path('group_success_signup/<int:pk>', views.SuccessSignup.as_view(), name='group_success_signup'),
]
