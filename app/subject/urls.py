from rest_framework.urls import path
from subject.views import SubjectsListView, SubjectDetailView

app_name = "subject"

urlpatterns = [
    path("", SubjectsListView.as_view(), name="subject-list"),
    path("<str:code>", SubjectDetailView.as_view(), name="subject-detail"),
]
