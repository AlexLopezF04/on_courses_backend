from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.filters import UserFilter
from courses.models import User
from courses.permissions import IsAdminUser, IsOwnerOrAdmin
from courses.serializers import UserSerializer, UserWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuarios.
    - List: solo administradores
    - Retrieve: dueño del perfil o admin
    - Create (registro): usar /api/auth/register/
    - Update: dueño del perfil o admin
    - Delete: solo administradores
    """
    queryset = User.objects.all()
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UserWriteSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAdminUser()]
