from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_admin, auth_client, unauth_client


class UserPermissionTests(TestCase):
    """Pruebas de permisos sobre usuarios."""

    def setUp(self):
        self.user = create_user("carlos")
        self.admin = create_admin()
        self.user_client = auth_client(self.user)
        self.admin_client = auth_client(self.admin)

    def test_regular_user_cannot_list_users(self):
        resp = self.user_client.get("/api/users/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        resp = self.admin_client.get("/api/users/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_user_can_get_own_profile(self):
        resp = self.user_client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["username"], "carlos")

    def test_user_cannot_get_other_profile(self):
        other = create_user("diana")
        resp = self.user_client.get(f"/api/users/{other.id}/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_gets_401(self):
        resp = unauth_client().get("/api/users/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
