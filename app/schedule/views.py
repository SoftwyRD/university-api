"""
Views for the schedule app
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import SectionSchedule as ScheduleModel


class ScheduleListView(APIView):
    """Schedule list view"""

    def get(self, request, format=None):
        """Get all schedules"""
        schedules = ScheduleModel.objects.all()
        serializer = self.serializer_class(schedules, many=True)
        response = {
            "status": "success",
            "data": {
                "schedules": serializer.data,
            },
        }
        return Response(response, status.HTTP_200_OK)
