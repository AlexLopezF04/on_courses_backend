from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.community.models import ForumThread, ForumPost, Announcement, LessonComment
from apps.community.serializers import (
    ForumThreadSerializer, ForumThreadDetailSerializer, ForumThreadWriteSerializer,
    ForumPostSerializer, ForumPostWriteSerializer,
    AnnouncementSerializer, AnnouncementWriteSerializer,
    LessonCommentSerializer, LessonCommentWriteSerializer
)
from apps.community.filters import ForumThreadFilter, AnnouncementFilter, LessonCommentFilter
from apps.community.permissions import IsProfessorOrAdminForAnnouncement
from apps.users.permissions import IsOwnerOrAdmin


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


class AnnouncementViewSet(viewsets.ModelViewSet):
    """CRUD de anuncios. Solo profesores y admin pueden crear/modificar."""
    queryset = Announcement.objects.all()
    filterset_class = AnnouncementFilter
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return AnnouncementWriteSerializer
        return AnnouncementSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsProfessorOrAdminForAnnouncement()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
