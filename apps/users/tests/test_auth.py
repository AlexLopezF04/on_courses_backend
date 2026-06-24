from django.core import mail
from django.test import TestCase
from rest_framework import status

from apps.helpers import create_user, create_admin, get_tokens, auth_client, unauth_client
from apps.users.models import User


class RegisterTests(TestCase):
    """Pruebas de registro de usuarios."""

    def setUp(self):
        self.client = unauth_client()
        self.url = '/api/auth/register/'
        self.data = {
            'username': 'john',
            'email': 'john@test.com',
            'password': 'Pass1234!',
            'password_confirm': 'Pass1234!',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_register_success(self):
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['username'], 'john')
        self.assertEqual(resp.data['role'], 'student')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Bienvenido', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['john@test.com'])

    def test_register_passwords_do_not_match(self):
        self.data['password_confirm'] = 'Different!'
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        create_user('john')
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        self.data['password'] = self.data['password_confirm'] = '123'
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(TestCase):
    """Pruebas de inicio de sesión."""

    def setUp(self):
        self.client = unauth_client()
        self.user = create_user('ana', password='Pass1234!')

    def test_login_success(self):
        resp = self.client.post('/api/auth/login/', {
            'username': 'ana', 'password': 'Pass1234!'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_login_invalid_credentials(self):
        resp = self.client.post('/api/auth/login/', {
            'username': 'ana', 'password': 'wrong'
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class RefreshTests(TestCase):
    """Pruebas de refresh de token JWT."""

    def setUp(self):
        self.client = unauth_client()
        user = create_user('bob')
        self.access, self.refresh = get_tokens(user)

    def test_refresh_returns_new_access(self):
        resp = self.client.post('/api/auth/refresh/', {'refresh': self.refresh})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
