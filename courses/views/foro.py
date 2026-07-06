from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import ForumThreadFilter
from courses.models import ForumPost, ForumThread
from courses.serializers import (
    ForumPostSerializer,
    ForumPostWriteSerializer,
    ForumThreadDetailSerializer,
    ForumThreadSerializer,
    ForumThreadWriteSerializer,
)


class ForumThreadViewSet(viewsets.ModelViewSet):
    """CRUD de hilos de foro por curso."""
    queryset = ForumThread.objects.all()
    filterset_class = ForumThreadFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ForumThreadDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ForumThreadWriteSerializer
        return ForumThreadSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ForumPostViewSet(viewsets.ModelViewSet):
    """CRUD de mensajes dentro de un hilo."""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ForumPostWriteSerializer
        return ForumPostSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
