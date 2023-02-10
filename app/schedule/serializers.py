from core.models import SubjectSection, Subject, Selection as SelectionModel
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class SelectionSerializer(ModelSerializer):
    """
    Selection Serializer
    """

    class Meta:
        model = SelectionModel
        fields = "__all__"
        read_only_fields = ["id"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


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
            "subject_code",
            "subject_name",
            "professor",
            "taken",
        ]

    def run_validation(self, data):
        super().run_validation(data)
        return data

    def create(self, validated_data):
        subject_id = validated_data["subject"]
        subject = Subject.objects.get(id=subject_id)

        validated_data["subject"] = subject
        subject_section = SubjectSection.objects.create(**validated_data)
        return subject_section

    def get_selection(self, obj):
        selection = obj.selection
        serializer = SelectionSerializer(selection, many=False)
        data = serializer.data
        selection = data["name"]
        return selection

    def get_subject_code(self, obj):
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_code = data["code"]
        return subject_code

    def get_subject_name(self, obj):
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_name = data["name"]
        return subject_name