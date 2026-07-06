from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import LessonFilter
from courses.models import Lesson
from courses.permissions import IsProfessorOrAdminForWrite, IsProfessorOwner
from courses.serializers import LessonSerializer, LessonDetailSerializer


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
