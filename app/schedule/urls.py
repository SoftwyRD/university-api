"""
Urls for the schedule app
"""

from django.urls import path

urlPatterns = [
    path("", views.ScheduleListView.as_view(), name="schedule-list"),
]
