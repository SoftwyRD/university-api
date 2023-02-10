from rest_framework import serializers
from core.models import Subject as SubjectModel


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = "__all__"
