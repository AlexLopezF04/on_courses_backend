from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.gamification.models import Achievement, UserAchievement, Review
from apps.gamification.serializers import (
    AchievementSerializer, UserAchievementSerializer,
    ReviewSerializer, ReviewWriteSerializer
)
from apps.gamification.filters import UserAchievementFilter, ReviewFilter
from apps.gamification.permissions import IsOwnerOrAdminForReview
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
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
