from rest_framework import serializers
from core.models import Selection as SelectionModel


class SelectionSerializer(serializers.ModelSerializer):
    """
    Selection Serializer
    """

    class Meta:
        model = SelectionModel
        fields = "__all__"
        read_only_fields = ["id"]
