from django.urls import path
from schedule import views

app_name = "schedule"

urlpatterns = [
    path(
        "<uuid:selection_id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subject-list",
    ),
    path(
        "<uuid:selection_id>/subjects/<int:subject_section_id>/",
        views.SubjectSectionDetailsView.as_view(),
        name="subject-details",
    ),
]
