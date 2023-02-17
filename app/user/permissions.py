"""User permissions."""

from rest_framework.permissions import BasePermission


class PublicPostRequest(BasePermission):
    """Allow only public post requests"""

    def has_permission(self, request, view):
        """Check if request is public post request"""
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_staff)


class IsPostRequest(BasePermission):
    """Allow only post requests"""

    def has_permission(self, request, view):
        """Check if request is post request"""
        return request.method == "POST"
