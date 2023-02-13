from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    RefreshToken,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "password",
            "email",
        ]
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
                "min_length": 8,
            },
        }

    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class PairTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            response = {
                "status": "success",
                "data": {
                    "tokens": data,
                },
            }

            return response
        except AuthenticationFailed as ex:
            response = {
                "status": "fail",
                "data": {
                    "title": "No active account",
                    "message": str(ex),
                },
            }

            raise AuthenticationFailed(response)


class RefreshTokenSerializer(RefreshToken):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            response = {
                "status": "success",
                "data": {
                    "token": data,
                },
            }

            return response
        except AuthenticationFailed as ex:
            response = {
                "status": "fail",
                "data": {
                    "title": ex.args[1],
                    "message": ex.args[0],
                },
            }

            raise AuthenticationFailed(response)
