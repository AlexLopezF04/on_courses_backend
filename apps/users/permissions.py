from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso solo al dueño del objeto o a usuarios administradores.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == 'admin'


class IsAdminUser(BasePermission):
    """Acceso exclusivo para administradores."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsProfessorOrAdmin(BasePermission):
    """Acceso para profesores y administradores."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ('professor', 'admin')


class ReadOnly(BasePermission):
    """Solo métodos GET, HEAD, OPTIONS."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
