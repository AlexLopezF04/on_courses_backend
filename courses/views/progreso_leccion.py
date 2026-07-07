from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.filters import LessonProgressFilter
from courses.models import LessonProgress
from courses.permissions import IsAdminUser, IsEnrolledOrAdmin
from courses.serializers import LessonProgressSerializer, LessonProgressWriteSerializer


class LessonProgressViewSet(viewsets.ModelViewSet):
    """CRUD de progreso de lecciones. Sincroniza avance de video."""

    queryset = LessonProgress.objects.all()
    filterset_class = LessonProgressFilter
    ordering_fields = ["updated_at"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return LessonProgressWriteSerializer
        return LessonProgressSerializer

    def get_permissions(self):
        if self.action in ("list",):
            return [IsAdminUser()]
        if self.action in ("retrieve",):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
