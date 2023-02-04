from rest_framework import status, views
from rest_framework.response import Response

from core.models import Subject as SubjectModel
from subject.serializers import SubjectSerializer


class Subjects(views.APIView):
    """Vieqw for list subjects in api"""

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
