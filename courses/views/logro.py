from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import UserAchievementFilter
from courses.models import Achievement, UserAchievement
from courses.permissions import IsAdminUser, IsProfessorOrAdmin
from courses.serializers import AchievementSerializer, UserAchievementSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    """CRUD de logros. Solo administradores pueden modificar."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    search_fields = ["name", "description"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdminUser()]


class UserAchievementViewSet(viewsets.ModelViewSet):
    """Logros obtenidos por los usuarios. Solo lectura para estudiantes."""

    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    filterset_class = UserAchievementFilter

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
