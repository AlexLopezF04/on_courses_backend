from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.gamification.filters import ReviewFilter, UserAchievementFilter
from apps.gamification.models import Achievement, Review, UserAchievement
from apps.gamification.permissions import IsOwnerOrAdminForReview
from apps.gamification.serializers import (
    AchievementSerializer,
    ReviewSerializer,
    ReviewWriteSerializer,
    UserAchievementSerializer,
)
from apps.users.permissions import IsAdminUser, IsProfessorOrAdmin


class AchievementViewSet(viewsets.ModelViewSet):
    """CRUD de logros. Solo administradores pueden modificar."""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]


class UserAchievementViewSet(viewsets.ModelViewSet):
    """Logros obtenidos por los usuarios. Solo lectura para estudiantes."""
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    filterset_class = UserAchievementFilter

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD de reseñas de cursos."""
    queryset = Review.objects.all()
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'created_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ReviewWriteSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsOwnerOrAdminForReview()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
