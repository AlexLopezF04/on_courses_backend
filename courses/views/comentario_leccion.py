from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import LessonCommentFilter
from courses.models import LessonComment
from courses.serializers import LessonCommentSerializer, LessonCommentWriteSerializer


class LessonCommentViewSet(viewsets.ModelViewSet):
    """CRUD de comentarios en lecciones. Soporta respuestas anidadas."""
    queryset = LessonComment.objects.all()
    filterset_class = LessonCommentFilter
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return LessonCommentWriteSerializer
        return LessonCommentSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
