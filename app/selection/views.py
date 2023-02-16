from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.serializers import SubjectSectionSerializer, SelectionSerializer
from core.models import SubjectSection, Selection as SelectionModel
from drf_spectacular.utils import extend_schema

from datetime import datetime


def subject_section_location_url(selection_id, subject_section_id):
    return reverse(
        "selection:subject-details", args=[selection_id, subject_section_id]
    )


class SubjectSectionListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None,
                   responses=SubjectSectionSerializer)
    def get(self, request, selection_id, format=None):
        try:
            user = request.user
            selection = SelectionModel.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find selection",
                        "message": "Could not find any matching"
                        + " selections to add this subject section.",
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
        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SubjectSectionSerializer,
                   responses=SubjectSectionSerializer)
    def post(self, request, selection_id, format=None):
        try:
            user = request.user
            selection = SelectionModel.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you are"
                        + " trying to add the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            data["selection"] = selection

            serializer = SubjectSectionSerializer(data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                subject_section = serializer.data

                headers = {
                    "Location": subject_section_location_url(
                        selection_id, subject_section["id"]
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
        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSectionDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None,
                   responses=SubjectSectionSerializer)
    def get(self, request, selection_id, subject_section_id, format=None):
        try:
            user = request.user
            selection = SelectionModel.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you"
                        + " are trying to get the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.get(id=subject_section_id)
            serializer = SubjectSectionSerializer(subject_section, many=False)
            response = {
                "status": "success",
                "data": {
                    "subject_section": serializer.data,
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SubjectSectionSerializer,
                   responses=SubjectSectionSerializer)
    def patch(self, request, selection_id, subject_section_id, format=None):
        try:
            user = request.user
            selection = SelectionModel.objects.get(id=selection_id)
            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you are"
                        + " trying to update the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            subject_section = SubjectSection.objects.get(id=subject_section_id)
            serializer = SubjectSectionSerializer(
                subject_section, data=data, many=False, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "data": {
                        "subject_section": serializer.data,
                    },
                }
                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the subject subject",
                    "details": serializer.errors,
                },
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to update the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, selection_id, subject_section_id, format=None):
        try:
            user = request.user
            selection = SelectionModel.objects.get(id=selection_id)
            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the subject",
                        "message": "Could not find the subject you are"
                        + " trying to delete.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.get(id=subject_section_id)
            subject_section.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = SelectionSerializer

    def get(self, req, format=None):
        try:
            selection = SelectionModel.objects.all().filter(user=req.user.id)

            serializer = self.serializer(selection, many=True)

            response = {
                "status": "success",
                "data": {
                    "count": selection.count(),
                    "selections": serializer.data,
                },
            }

            return Response(response, status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SelectionSerializer,
                   responses=SelectionSerializer)
    def post(self, req, format=None):
        try:
            selection = {
                "user": req.user.id,
                "name": req.data["name"],
            }
            serializer = self.serializer(data=selection, many=False)

            if serializer.is_valid():
                serializer.save()

                selection = serializer.data

                response = {
                    "status": "success",
                    "data": {
                        "selection": selection,
                    },
                }
                return Response(response, status.HTTP_201_CREATED)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create selection",
                    "details": serializer.errors,
                },
            }
            print(serializer.errors)
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SelectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = SelectionSerializer

    @extend_schema(request=None,
                   responses=SelectionSerializer)
    def get(self, req, id, format=None):
        try:
            selection = SelectionModel.objects.filter(id=id)[0]
            serialized = self.serializer(selection, many=False)

            if selection and serialized.data["user"] == req.user.id:

                response = {
                    "status": "success",
                    "data": {
                        "selection": serialized.data,
                    },
                }

                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "selection does not exist",
                    "message": "Could not find any matching"
                    + " selection.",

                },
            }

            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SelectionSerializer,
                   responses=SelectionSerializer)
    def patch(self, req, id, format=None):
        try:
            selectionQuery = SelectionModel.objects.filter(id=id)
            if selectionQuery:
                serializedQuerry = self.serializer(
                    selectionQuery[0], many=False
                )

            if selectionQuery and serializedQuerry.data["user"] == req.user.id:
                selection = SelectionModel.objects.get(id=id)
                data = dict(req.data)

                data["modified_on"] = datetime.now()
                serializer = self.serializer(
                    selection, data=req.data, many=False, partial=True
                )

                if serializer.is_valid():
                    serializer.save()

                    response = {
                        "status": "success",
                        "data": {
                            "selection": serializer.data,
                        },
                    }
                    return Response(response, status.HTTP_200_OK)

                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not update the selection",
                        "message": serializer.errors,
                    },
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the selection",
                    "message": "Could not find any matching"
                    + " selection.",
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
            selection = SelectionModel.objects.filter(id=id)
            if selection:
                serialized = self.serializer(selection[0], many=False)

            if selection and serialized.data["user"] == req.user.id:
                selection = SelectionModel.objects.get(id=id)
                selection.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

            response = {
                "status": "fail",
                "data": {
                    "title": "Selection does not exist",
                    "message": "Could not find any matching"
                    + " selection.",
                },
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
