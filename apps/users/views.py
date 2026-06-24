from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint de verificación del servidor.
    Retorna 200 OK si el sistema está funcionando correctamente.
    """
    return Response({'status': 'ok', 'version': '1.0'})
