from rest_framework.permissions import BasePermission

from rod.common.utils import user_in_group


class IsSupportAgent(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Support Agent")


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Product Admin")


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Customer")


class IsProductAdminOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Product Admin") or user_in_group(
            request.user,
            "Customer",
        )
