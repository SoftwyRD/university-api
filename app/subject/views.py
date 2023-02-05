from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Subject as SubjectModel
from subject.serializers import SubjectSerializer
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


class Subjects(views.APIView):
    """View for list subjects in api"""
    permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]

    def get(self, req, format=None):
        subjects = SubjectModel.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        response = {
            "status": "success",
            "data": {
                "count": subjects.count(),
                "subjects": serializer.data,
            }
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, req, format=None):
