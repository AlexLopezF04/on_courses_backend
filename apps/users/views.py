from drf_spectacular.utils import extend_schema
from rest_framework import APIView, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.email_helper import send_welcome_email
from apps.users.filters import UserFilter
from apps.users.models import User
from apps.users.permissions import IsAdminUser, IsOwnerOrAdmin
from apps.users.serializers import RegisterSerializer, UserSerializer, UserWriteSerializer


@extend_schema(request=None, responses={200: None})
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Verifica que el servidor esté operativo."""
    return Response({'status': 'ok', 'version': '1.0'})


class RegisterView(generics.CreateAPIView):
    """Registro público de nuevos usuarios (rol 'student' por defecto)."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email(user)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


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

class LogoutView(APIView):
    """Cierra sesión e invalida el token refresh."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response(
                {"error": "Se requiere el token refresh"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"error": "Token inválido o ya expirado"},
                status=status.HTTP_400_BAD_REQUEST,
            )