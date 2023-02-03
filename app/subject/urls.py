from django.urls import path
from subject.views import Subjects

app_name = 'subject'

urlpatterns = [
    path('', Subjects.as_view(), name='subject-list')
]
