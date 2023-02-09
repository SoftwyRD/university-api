from schedule import views
from rest_framework.urls import path

app_name = "schedule"


urlpatterns = [
    path('', views.SelectionListView.as_view(), name='selection-list'),
    path('<str:id>', views.SelectionDetailView.as_view(),
         name='selection-detail')
]
