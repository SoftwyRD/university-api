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
    selection = SerializerMethodField(read_only=True)
    subject = SerializerMethodField(read_only=True)

    class Meta:
        model = SubjectSection
        fields = "__all__"

    def get_selection(self, obj):
        selection = obj.selection
        serializer = SelectionSerializer(selection, many=False)
        return serializer.data["name"]

    def get_subject(self, obj):
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        subject_name = f"{serializer.data['code']} - {serializer.data['name']}"
        return subject_name
