from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user import serializers

# Create your views here.


class PairTokenView(TokenObtainPairView):
    serializer_class = serializers.PairTokenSerializer


class RefreshTokenView(TokenRefreshView):
    serializer_class = serializers.RefreshTokenSerializer


class UserListView(APIView):
    permission_classes = [IsAdminUser]
    serializer = serializers.UserSerializer

    def get(self, request, format=None):
        try:
            users = get_user_model().objects.all()
            serializer = self.serializer(users, many=True)

            response = {
                "status": "success",
                "data": {
                    "count": users.count(),
                    "users": serializer.data,
                },
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            serializer = self.serializer(data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "data": {
                        "user": serializer.data,
                    },
                }
                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not register the user",
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


class UserDetailsView(APIView):
    permission_classes = [IsAdminUser]
    serializer = serializers.UserSerializer

    def get_object(self, id):
        try:
            user = get_user_model().objects.get(id=id)
            serializer = self.serializer(user, many=False)

            response = {
                "status": "success",
                "data": {
                    "user": serializer.data,
                },
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id, format=None):
        try:
            data = request.data
            user = get_user_model().objects.get(id=id)
            serializer = self.serializer(user, data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                return Response(status.HTTP_204_NO_CONTENT)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the user",
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

    def delete(self, request, id, format=None):
        try:
            user = get_user_model().objects.get(id=id)
            user.delete()

            return Response(status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
