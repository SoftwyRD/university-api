from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    BasePermission,
    SAFE_METHODS,
)

from core.models import Subject as SubjectModel
from subject.serializers import SubjectSerializer
from drf_spectacular.utils import extend_schema


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SubjectsListView(views.APIView):
    """View for list subjects in api"""

    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = SubjectSerializer

    @extend_schema(request=None, responses=SubjectSerializer)
    def get(self, req, format=None):
        try:
            subjects = SubjectModel.objects.all()
            serializer = self.serializer_class(subjects, many=True)
            response = {
                "status": "success",
                "data": {
                    "count": subjects.count(),
                    "subjects": serializer.data,
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SubjectSerializer, responses=SubjectSerializer)
    def post(self, req, format=None):
        try:
            data = req.data
            serializer = self.serializer_class(data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                subject = serializer.data

                response = {
                    "status": "success",
                    "data": {
                        "subject": subject,
                    },
                }
                return Response(response, status.HTTP_201_CREATED)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create this subject",
                    "message": serializer.errors,
                },
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectDetailView(views.APIView):
    """
    View for GET, PUT and PATCH subject details
    """

    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = SubjectSerializer

    @extend_schema(request=None, responses=SubjectSerializer)
    def get(self, req, id, format=None):
        try:
            if SubjectModel.objects.filter(id=id):
                subject = SubjectModel.objects.get(id=id)
                serializer = self.serializer_class(subject, many=False)

                response = {
                    "status": "success",
                    "data": {
                        "subject": serializer.data,
                    },
                }

                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "Subject does not exist",
                    "message": "Could not find any matching" + " subject.",
                },
            }

            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SubjectSerializer, responses=SubjectSerializer)
    def patch(self, req, id, format=None):
        try:
            if SubjectModel.objects.filter(id=id):
                subject = SubjectModel.objects.get(id=id)
                data = req.data

                serializer = self.serializer_class(
                    subject, data=data, many=False, partial=True
                )

                if serializer.is_valid():
                    serializer.save()

                    return Response(status=status.HTTP_204_NO_CONTENT)

                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not update the subject",
                        "message": serializer.errors,
                    },
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            response = {
                "status": "fail",
                "data": {
                    "title": "Subject does not exist",
                    "message": "Could not find any matching" + " subject.",
                },
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, req, id, format=None):
        try:
            if SubjectModel.objects.filter(id=id):
                subject = SubjectModel.objects.get(id=id)
                subject.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

            response = {
                "status": "fail",
                "data": {
                    "title": "Subject does not exist",
                    "message": "Could not find any matching" + " subject.",
                },
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
