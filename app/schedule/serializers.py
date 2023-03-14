"""
Serializers for the schedule app

"""

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from core.models import SectionSchedule as ScheduleModel


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = ScheduleModel
        fields = "__all__"
