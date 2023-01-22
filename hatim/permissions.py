from rest_framework import permissions


class HatimCountPermission(permissions.BasePermission):
    message = 'User exceeded object limit'
    
    def has_permission(self, request, view):
        user = request.user
        if bool(request.user and request.user.is_authenticated):
            if user.active_hatims == 0:
                return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id == request.user


class IsOwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user