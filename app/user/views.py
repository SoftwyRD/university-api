from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.serializers import PairTokenSerializer, RefreshTokenSerializer

# Create your views here.


class PairTokenView(TokenObtainPairView):
    serializer_class = PairTokenSerializer


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer
