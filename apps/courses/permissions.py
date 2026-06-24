from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfessorOwner(BasePermission):
    """
    Permite modificar solo los cursos que le pertenecen al profesor.
    Los administradores pueden modificar cualquier curso.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'professor':
            # Verifica si el objeto tiene 'professor' o 'course.professor'
            professor = getattr(obj, 'professor', None)
            if professor is None:
                course = getattr(obj, 'course', None)
                if course:
                    professor = course.professor
            return professor == request.user
        return False


class IsProfessorOrAdminForWrite(BasePermission):
    """
    Permite lectura a cualquiera, escritura solo a profesores y admins.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.role in ('professor', 'admin')
