from rest_framework.permissions import BasePermission


class PublicPostRequest(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_staff)


class IsPostRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"
