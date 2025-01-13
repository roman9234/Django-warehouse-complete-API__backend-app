from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
    Allows access only to non-authenticated users.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsNotAuthenticatedOrAdmin(BasePermission):
    """
    Разрешает доступ либо неавторизованным пользователям,
    либо администраторам.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated or request.user.is_staff


class IsRequesterOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return not request.user.is_supplier or request.user.is_staff
        else:
            return False

class IsSupplierOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_supplier or request.user.is_staff
        else:
            return False