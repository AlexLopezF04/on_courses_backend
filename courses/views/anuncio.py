from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.filters import AnnouncementFilter
from courses.models import Announcement
from courses.permissions import IsProfessorOrAdminForAnnouncement
from courses.serializers import AnnouncementSerializer, AnnouncementWriteSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """CRUD de anuncios. Solo profesores y admin pueden crear/modificar."""

    queryset = Announcement.objects.all()
    filterset_class = AnnouncementFilter
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return AnnouncementWriteSerializer
        return AnnouncementSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsProfessorOrAdminForAnnouncement()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
