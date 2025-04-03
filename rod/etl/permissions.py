from rest_framework.permissions import BasePermission


class IsSupportAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Support Agent").exists()


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Product Admin").exists()
