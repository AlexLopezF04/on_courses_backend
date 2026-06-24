from django.test import TestCase
from rest_framework import status

from apps.helpers import create_user, create_admin, auth_client, unauth_client
from apps.courses.tests.helpers import create_category


class CategoryPermissionTests(TestCase):
    """Pruebas de permisos sobre categorías."""

    def setUp(self):
        self.student = create_user('eve')
        self.admin = create_admin()
        self.category = create_category()

    def test_anyone_can_list_categories(self):
        resp = unauth_client().get('/api/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create_category(self):
        resp = auth_client(self.student).post('/api/categories/', {
            'name': 'Test', 'slug': 'test'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_category(self):
        resp = auth_client(self.admin).post('/api/categories/', {
            'name': 'Frontend', 'slug': 'frontend'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_category(self):
        resp = auth_client(self.admin).delete(f'/api/categories/{self.category.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
