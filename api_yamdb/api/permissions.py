from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role != 'admin':
            return False

    def has_object_permission(self, request, view, obj):
        return True


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )


class AuthorEditOrReadAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        )
