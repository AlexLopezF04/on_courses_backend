from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.courses.models import Category, Course, Module, Lesson, Resource
from apps.courses.serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    CourseWriteSerializer, ModuleSerializer, LessonSerializer,
    LessonDetailSerializer, ResourceSerializer
)
from apps.courses.filters import CourseFilter, ModuleFilter, LessonFilter
from apps.courses.permissions import IsProfessorOrAdminForWrite, IsProfessorOwner
from apps.users.permissions import IsAdminUser


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD de categorías. Lectura pública, escritura solo admin."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]


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
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseWriteSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsProfessorOrAdminForWrite()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Course.objects.all()
        if self.action in ('list', 'retrieve'):
            if self.request.user.is_authenticated:
                return qs
            return qs.filter(is_active=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)


class ModuleViewSet(viewsets.ModelViewSet):
    """CRUD de módulos. Anidados lógicamente a un curso."""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filterset_class = ModuleFilter
    ordering_fields = ['order']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]

    def perform_create(self, serializer):
        serializer.save()


class LessonViewSet(viewsets.ModelViewSet):
    """CRUD de lecciones."""
    queryset = Lesson.objects.all()
    filterset_class = LessonFilter
    ordering_fields = ['order']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]


class ResourceViewSet(viewsets.ModelViewSet):
    """CRUD de recursos descargables."""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]
