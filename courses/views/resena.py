from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import ReviewFilter
from courses.models import Review
from courses.permissions import IsOwnerOrAdminForReview
from courses.serializers import ReviewSerializer, ReviewWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD de reseñas de cursos."""

    queryset = Review.objects.all()
    filterset_class = ReviewFilter
    ordering_fields = ["rating", "created_at"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ReviewWriteSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsOwnerOrAdminForReview()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
