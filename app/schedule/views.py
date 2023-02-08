from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Selection as SelectionModel
from schedule.serializers import SelectionSerializer
from user.serializers import UserSerializer
# Create your views here.


class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = SelectionSerializer

    def post(self, req, format=None):
        selection = dict(req.data)

        # selection["user"] = req.user
        selection["name"] = "AAAAAAAAAAAa"
        # print(selection)
        serializer = self.serializer(data=selection, many=False)
        # print(serializer.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

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

    def get(self, req, format=None):
        selection = SelectionModel.objects.all()

        serializer = self.serializer(selection, many=True)

        response = {
            "status": "success",
            "data": {
                "selection": serializer.data,
            },
        }

        return Response(response, status.HTTP_200_OK)
