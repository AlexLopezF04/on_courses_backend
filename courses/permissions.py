from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso solo al dueño del objeto o a usuarios administradores.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == "admin"


class IsAdminUser(BasePermission):
    """Acceso exclusivo para administradores."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsProfessorOrAdmin(BasePermission):
    """Acceso para profesores y administradores."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ("professor", "admin")


class ReadOnly(BasePermission):
    """Solo métodos GET, HEAD, OPTIONS."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsProfessorOwner(BasePermission):
    """
    Permite modificar solo los cursos que le pertenecen al profesor.
    Los administradores pueden modificar cualquier curso.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ("professor", "admin")

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if request.user.role == "professor":
            professor = getattr(obj, "professor", None)
            if professor is None:
                course = getattr(obj, "course", None)
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
        return request.user.role in ("professor", "admin")


class IsProfessorOrAdminForAnnouncement(BasePermission):
    """
    Solo el profesor dueño del curso o un admin pueden crear/modificar anuncios.
    Lectura permitida a cualquiera autenticado.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in ("professor", "admin")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == "admin":
            return True
        return obj.author == request.user


class IsEnrolledOrAdmin(BasePermission):
    """
    Permite ver progreso solo al estudiante dueño del progreso o al admin.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj.user == request.user


class IsProfessorOfCourse(BasePermission):
    """
    Permite modificar evaluaciones/preguntas solo al profesor dueño del curso.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        course = getattr(obj, "course", None)
        return course and course.professor == request.user


class IsOwnerOrAdminForReview(BasePermission):
    """Solo el autor de la reseña o un admin pueden modificarla."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.role == "admin"


class IsOwnerOfTicket(BasePermission):
    """Solo el dueño del ticket o un admin pueden ver/modificar."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj.user == request.user


class IsAdminOrSelfForOrder(BasePermission):
    """Solo el comprador o un admin pueden ver la orden."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj.user == request.user
