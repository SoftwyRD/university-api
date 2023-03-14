"""Selection URL Configuration"""

from selection import views
from rest_framework.urls import path

app_name = "selection"


urlpatterns = [
    path("", views.SelectionListView.as_view(), name="selection-list"),
    path(
        "<uuid:id>",
        views.SelectionDetailView.as_view(),
        name="selection-detail",
    ),
    path(
        "<uuid:selection_id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subject-list",
    ),
    path(
        "<uuid:selection_id>/sections/<int:subject_section_id>/",
        views.SubjectSectionDetailsView.as_view(),
        name="subject-detail",
    ),
    path(
        "<uuid:selection_id>/subjects/<int:subject_section_id>/schedules/",
        views.SubjectSectionDetailsView.as_view(),
        name="schedule-list",
    ),
    path(
        "<uuid:selection_id>/subjects/<int:subject_section_id>/schedules/<int:schedule_id>/",
        views.SubjectSectionDetailsView.as_view(),
        name="schedule-detail",
    ),
]
