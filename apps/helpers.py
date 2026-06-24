from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_user(username='student', password='Pass1234!', role='student', **kwargs):
    """Crea un usuario de prueba con el rol especificado."""
    return User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        password=password,
        role=role,
        **kwargs
    )


def create_professor(username='prof', password='Pass1234!'):
    """Crea un profesor de prueba."""
    return create_user(username=username, password=password, role='professor')


def create_admin(username='admin', password='Pass1234!'):
    """Crea un administrador de prueba."""
    return create_user(username=username, password=password, role='admin')


def get_tokens(user):
    """Obtiene tokens JWT de acceso y refresh."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def auth_client(user):
    """Retorna un APIClient autenticado con JWT."""
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


def unauth_client():
    """Retorna un APIClient sin autenticación."""
    return APIClient()
