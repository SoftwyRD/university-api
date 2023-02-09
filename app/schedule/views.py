from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from core.models import Selection as SelectionModel
from schedule.serializers import SelectionSerializer
from user.serializers import UserSerializer
# Create your views here.


def create_user(first_name="first_name",
                last_name="last_name",
                email="user@example.com",
                username="username",
                password="password"):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "username": username,
        "password": password,
    }
    user = get_user_model().objects.create(**data)
    return user


class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = SelectionSerializer

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
                "status": "failed",
                "data": {
                    "selection": serializer.errors,
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


class SelectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = SelectionSerializer

    def get(self, req, id, format=None):
        try:
            # selection = SelectionModel.objects.get(id=id)
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
                    "selection": "selection does not exist",
                },
            }

            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            response = {
                "status": "error",
                "data": {
                    "message": ex,
                },
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, req, id, format=None):
        try:
            # selection = SelectionModel.objects.get(id=id)
            selectionQuery = SelectionModel.objects.filter(id=id)
            if selectionQuery:
                serializedQuerry = self.serializer(
                    selectionQuery[0], many=False)

            if selectionQuery and serializedQuerry.data["user"] == req.user.id:
                selection = SelectionModel.objects.get(id=id)
                # payload = {}
                # selection = dict(req.data)

                # for a in selection:
                #     payload[a] = selection[a][0]

                # print(payload)
                serializer = self.serializer(
                    selection, data=req.data, many=False, partial=True)

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
                        "title": "Could not update the user",
                        "message": serializer.errors,
                    },
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

            response = {
                "status": "fail",
                "message": "selection does not exist",
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "data": {
                    "message": ex,
                },
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, req, id, format=None):
        try:
            # selection = SelectionModel.objects.get(id=id)
            selection = SelectionModel.objects.filter(id=id)
            if selection:
                serialized = self.serializer(selection[0], many=False)

            if selection and serialized.data["user"] == req.user.id:
                selection = SelectionModel.objects.get(id=id)
                selection.delete()

                response = {
                    "status": "success",
                    "data": "Selection deleted",
                }

                return Response(response, status.HTTP_204_NO_CONTENT)

            response = {
                "status": "fail",
                "message": "selection does not exist",
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "data": {
                    "message": ex,
                },
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
