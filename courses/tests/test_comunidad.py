from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_professor, create_admin, auth_client, unauth_client
from courses.tests.helpers import create_category, create_course


class ForumThreadTests(TestCase):
    """Pruebas de hilos de foro."""

    def setUp(self):
        self.student = create_user("gina")
        self.client = auth_client(self.student)
        cat = create_category()
        self.course = create_course(cat, create_professor())

    def test_create_thread(self):
        resp = self.client.post(
            "/api/forum-threads/",
            {
                "course": self.course.id,
                "title": "Duda sobre el curso",
                "content": "Tengo una pregunta...",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_list_threads_public(self):
        resp = unauth_client().get("/api/forum-threads/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
