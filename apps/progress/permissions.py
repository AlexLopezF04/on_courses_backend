from rest_framework.permissions import BasePermission


class IsEnrolledOrAdmin(BasePermission):
    """
    Permite ver progreso solo al estudiante dueño del progreso o al admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user


class IsProfessorOfCourse(BasePermission):
    """
    Permite modificar evaluaciones/preguntas solo al profesor dueño del curso.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        course = getattr(obj, 'course', None)
        return course and course.professor == request.user
