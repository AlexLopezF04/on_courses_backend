from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfessorOrAdminForAnnouncement(BasePermission):
    """
    Solo el profesor dueño del curso o un admin pueden crear/modificar anuncios.
    Lectura permitida a cualquiera autenticado.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in ('professor', 'admin')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == 'admin':
            return True
        return obj.author == request.user
