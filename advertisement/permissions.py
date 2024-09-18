from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """Правило проверки, является ли текущий пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False

