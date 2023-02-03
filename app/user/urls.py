from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("login/", views.PairTokenView().as_view(), name="token"),
    path(
        "login/refresh/",
        views.RefreshTokenView().as_view(),
        name="refresh-token",
    ),
]
