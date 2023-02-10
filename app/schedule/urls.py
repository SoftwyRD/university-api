from schedule import views
from rest_framework.urls import path

app_name = "schedule"


urlpatterns = [
    path('', views.SelectionListView.as_view(), name='selection-list'),
    path('<str:id>', views.SelectionDetailView.as_view(),
         name='selection-detail'),
    path(
        "<uuid:selection_id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subject-list",
    ),
    path(
        "<uuid:selection_id>/subjects/<int:subject_section_id>/",
        views.SubjectSectionDetailsView.as_view(),
        name="subject-details",
    )
]
