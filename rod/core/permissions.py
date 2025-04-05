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


class IsInAllowedGroups(BasePermission):
    """
    Check if the user is in one of the allowed groups.
    """

    allowed_groups = []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and any(user_in_group(request.user, group) for group in self.allowed_groups)
        )


class IsProductAdminOrCustomer(IsInAllowedGroups):
    allowed_groups = ["Product Admin", "Customer"]
