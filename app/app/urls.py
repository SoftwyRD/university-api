"""Urls for the app"""

from django.contrib import admin

from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/users/", include("user.urls"), name="users-resource"),
    path("api/subjects/", include("subject.urls"), name="subject-resource"),
    path(
        "api/selections/", include("selection.urls"), name="selection-resource"
    ),
]
