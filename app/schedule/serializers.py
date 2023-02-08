from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import SubjectSection, Selection, Subject
from user.serializers import UserSerializer


class SelectionSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)

    class Meta:
        model = Selection
        fields = ["id", "name", "user"]

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data["first_name"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectSectionSerializer(ModelSerializer):
    subject_code = SerializerMethodField()
    subject_name = SerializerMethodField()
    subject = SerializerMethodField()

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
