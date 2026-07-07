from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import CourseFilter
from courses.models import Course
from courses.permissions import IsAdminUser, IsProfessorOrAdminForWrite, IsProfessorOwner
from courses.serializers import CourseDetailSerializer, CourseListSerializer, CourseWriteSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD de cursos.
    - Lectura: pública (solo activos para students)
    - Creación: profesores y admins
    - Actualización: dueño del curso o admin
    - Eliminación: solo admin
    """

    queryset = Course.objects.all()
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["title", "price", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseWriteSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), IsProfessorOrAdminForWrite()]
        if self.action in ("update", "partial_update"):
            return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Course.objects.all()
        if self.action in ("list", "retrieve"):
            if self.request.user.is_authenticated:
                return qs
            return qs.filter(is_active=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)
