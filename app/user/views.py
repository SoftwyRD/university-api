"""User views"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user import serializers
from user.permissions import PublicPostRequest
from drf_spectacular.utils import extend_schema

schema_name = "user"


def user_location_url(user_id):
    """Get reverse url for user details"""

    return reverse("user:details", args=[user_id])


@extend_schema(
    tags=[schema_name],
)
class PairTokenView(TokenObtainPairView):
    """View for getting acces and refresh token for user"""

    serializer_class = serializers.PairTokenSerializer


@extend_schema(
    tags=[schema_name],
)
class RefreshTokenView(TokenRefreshView):
    """View for refreshing access token for user"""

    serializer_class = serializers.RefreshTokenSerializer


@extend_schema(tags=[schema_name])
class UserListView(APIView):
    """View for list users in api"""

    permission_classes = [PublicPostRequest]
    serializer_class = serializers.UserSerializer

    @extend_schema(
        request=None,
        responses=serializers.UserSerializer,
        operation_id="users_list_retrieve",
    )
    def get(self, request, format=None):
        """Get all users"""

        try:
            users = get_user_model().objects.all()
            serializer = self.serializer_class(users, many=True)

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

    @extend_schema(
        request=serializers.UserSerializer,
        responses=serializers.UserSerializer,
        operation_id="user_create",
    )
    def post(self, request, format=None):
        """Create new user"""

        try:
            data = request.data
            serializer = self.serializer_class(data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                user = serializer.data

                headers = {
                    "Location": user_location_url(user["id"]),
                }
                response = {
                    "status": "success",
                    "data": {
                        "user": user,
                    },
                }
                return Response(
                    response, status.HTTP_201_CREATED, headers=headers
                )

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


@extend_schema(tags=[schema_name])
class UserDetailsView(APIView):
    """View for user details in api"""

    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserSerializer

    @extend_schema(
        request=None,
        responses=serializers.UserSerializer,
        operation_id="user_details_retrieve",
    )
    def get(self, request, id, format=None):
        """Get user details"""

        try:
            user = get_user_model().objects.get(id=id)
            serializer = self.serializer_class(user, many=False)

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

    @extend_schema(
        request=serializers.UserSerializer,
        responses=serializers.UserSerializer,
        operation_id="user_update",
    )
    def patch(self, request, id, format=None):
        """Update user details"""

        try:
            data = request.data
            user = get_user_model().objects.get(id=id)
            serializer = self.serializer_class(user, data=data, many=False)

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

    @extend_schema(
        request=None,
        responses=None,
        operation_id="user_delete",
    )
    def delete(self, request, id, format=None):
        """Delete user"""

        try:
            user = get_user_model().objects.get(id=id)
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=[schema_name])
class MeView(APIView):
    """View for logged user details in api"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    @extend_schema(
        request=None,
        responses=serializers.UserSerializer,
        operation_id="me_retrieve",
    )
    def get(self, request, format=None):
        """Get logged user details"""
        user = request.user
        serializer = self.serializer_class(user, many=False)
        response = {
            "status": "success",
            "data": {
                "profile": serializer.data,
            },
        }
        return Response(response, status.HTTP_200_OK)

    @extend_schema(
        request=serializers.UserSerializer,
        responses=serializers.UserSerializer,
        operation_id="me_update",
    )
    def patch(self, request, format=None):
        """Update logged user details"""

        try:
            data = request.data
            user = request.user
            serializer = self.serializer_class(
                user, data=data, many=False, partial=True
            )

            if serializer.is_valid():
                serializer.save()

                response = {
                    "status": "success",
                    "data": {
                        "profile": serializer.data,
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
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
