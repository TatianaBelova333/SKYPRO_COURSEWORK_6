from rest_framework import permissions


class IsAdminOrAdOwner(permissions.BasePermission):
    message = 'Ads can be updated by ad owner or admin only.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_user and obj.author != request.user:
            return False
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
