from django.urls import path
from schedule import views

app_name = "schedule"

urlpatterns = [
    path(
        "<int:id>/subjects/",
        views.SubjectSectionView.as_view(),
        name="subject-list",
    ),
]
