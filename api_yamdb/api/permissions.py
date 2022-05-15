from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        return (
            user.role == 'admin' or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.role == 'admin' or user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff
        ):
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff
        ):
            return request.user.role == 'admin'
        return False


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_anonymous
            and request.method in permissions.SAFE_METHODS
        ):
            return True
        return (
            request.user.is_authenticated
            and request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
