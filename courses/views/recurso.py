from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.models import Resource
from courses.permissions import IsProfessorOrAdminForWrite, IsProfessorOwner
from courses.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """CRUD de recursos descargables."""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdminForWrite(), IsProfessorOwner()]
