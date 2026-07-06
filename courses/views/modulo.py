from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import ModuleFilter
from courses.models import Module
from courses.permissions import IsProfessorOrAdminForWrite, IsProfessorOwner
from courses.serializers import ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    """CRUD de módulos. Anidados lógicamente a un curso."""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filterset_class = ModuleFilter
    ordering_fields = ['order']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]

    def perform_create(self, serializer):
        serializer.save()
