from rest_framework import permissions

class AllowUnauthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
