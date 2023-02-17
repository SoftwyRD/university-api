"""Subject serializers."""

from rest_framework import serializers
from core.models import Subject as SubjectModel


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject"""

    class Meta:
        model = SubjectModel
        fields = "__all__"
        read_only_fields = ["id"]
