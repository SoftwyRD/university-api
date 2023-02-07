from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from schedule.serializers import SubjectSectionSerializer
from core.models import SubjectSection, Selection

# Create your views here.


def subject_section_location_url(subject_section_id):
    return reverse("schedule:subject-details", args=[subject_section_id])


class SubjectSectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            user = request.user
            selection = Selection.objects.get(id=id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find ",
                        "message": "",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.filter(
                selection=selection
            )
            serializer = SubjectSectionSerializer(subject_section, many=True)
            response = {
                "status": "success",
                "data": {
                    "count": subject_section.count(),
                    "subject_sections": serializer.data,
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id, format=None):
        try:
            subject_section = request.user
            selection = Selection.objects.get(id=id)

            if selection.user != subject_section:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find ",
                        "message": "",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            serializer = SubjectSectionSerializer(data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                subject_section = serializer.data

                headers = {
                    "Location": subject_section_location_url(
                        subject_section["id"]
                    ),
                }
                response = {
                    "status": "success",
                    "data": {
                        "subject_section": subject_section,
                    },
                }
                return Response(
                    response, status.HTTP_201_CREATED, headers=headers
                )

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create the subject section",
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
