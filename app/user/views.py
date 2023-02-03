from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
