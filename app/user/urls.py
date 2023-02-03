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
    path("", views.UserListView().as_view(), name="user-list"),
    path("<int:id>/", views.UserDetailsView().as_view(), name="user-details"),
    path("me/", views.MeView().as_view(), name="me"),
]
