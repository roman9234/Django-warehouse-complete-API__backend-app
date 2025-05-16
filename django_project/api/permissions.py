"""
Файл содержит классы разрешений приложения
"""
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
    """
    Разрешает доступ только заказчику или админу
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return not request.user.is_supplier or request.user.is_staff
        return False


class IsRequesterOfProduct(BasePermission):
    """
    Разрешает доступ только заказчику продукта
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsSupplierOrAdmin(BasePermission):
    """
    Разрешает доступ только поставщику или админу
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_supplier or request.user.is_staff
        return False


class IsSupplierOfProduct(BasePermission):
    """
    Разрешает доступ только поставщику этого продукта.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.product.producer == request.user
