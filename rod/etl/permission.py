from rest_framework.permissions import BasePermission


class CanViewCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_staff:
            return False
        if not hasattr(user, "employee"):
            return False
        return user.has_perm("etl.view_customer")
