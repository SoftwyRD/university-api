from rest_framework.serializers import ModelSerializer
from core.models import SubjectSection


class SubjectSectionSerializer(ModelSerializer):
    class Meta:
        model = SubjectSection
        fields = "__all__"
