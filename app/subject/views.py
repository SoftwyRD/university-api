from rest_framework import status, views
from rest_framework.response import Response

from core.models import Subject as SubjectModel
from subject.serializers import SubjectSerializer


class Subjects(views.APIView):
    """Vieqw for list subjects in api"""
    subjects = SubjectModel.objects.all()

    def get(self, req, format=None):
        return Response(self.subjects)
