from core.models import SubjectSection, Subject, Selection as SelectionModel
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Field,
)
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


@extend_schema_field(OpenApiTypes.NONE)
class MyField(Field):
    pass


class SelectionSerializer(ModelSerializer):
    """
    Selection Serializer
    """

    user = MyField()

    class Meta:
        model = SelectionModel
        fields = "__all__"
        read_only_fields = ["id", "created_on"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ["id"]


class SubjectSectionSerializer(ModelSerializer):
    subject_code = SerializerMethodField()
    subject_name = SerializerMethodField()
    selection = SerializerMethodField()

    class Meta:
        model = SubjectSection
        fields = [
            "id",
            "selection",
            "section",
            "subject",
            "subject_code",
            "subject_name",
            "professor",
            "taken",
        ]
        extra_kwargs = {
            "subject": {
                "write_only": True,
            }
        }
        read_only_fields = ["id"]

    def run_validation(self, data):
        super().run_validation(data)
        return data

    def create(self, validated_data):
        subject_id = validated_data["subject"]
        subject = Subject.objects.get(id=subject_id)

        validated_data["subject"] = subject
        subject_section = SubjectSection.objects.create(**validated_data)
        return subject_section

    def get_selection(self, obj) -> str:
        selection = obj.selection
        serializer = SelectionSerializer(selection, many=False)
        data = serializer.data
        selection = data["name"]
        return selection

    def get_subject_code(self, obj) -> str:
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_code = data["code"]
        return subject_code

    def get_subject_name(self, obj) -> str:
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_name = data["name"]
        return subject_name
