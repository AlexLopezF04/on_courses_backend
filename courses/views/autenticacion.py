from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from email_helper import send_welcome_email
from courses.models import User
from courses.serializers import RegisterSerializer, UserSerializer


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
