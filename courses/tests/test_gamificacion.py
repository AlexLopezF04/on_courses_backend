from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_admin, auth_client, unauth_client
from courses.tests.helpers import create_category, create_course


class ReviewTests(TestCase):
    """Pruebas de reseñas."""

    def setUp(self):
        self.student = create_user("iris")
        self.client = auth_client(self.student)
        cat = create_category()
        course = create_course(cat, create_user("prof2", role="professor"))
        self.course = course

    def test_create_review(self):
        resp = self.client.post("/api/reviews/", {"course": self.course.id, "rating": 4})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_invalid_rating_fails(self):
        resp = self.client.post("/api/reviews/", {"course": self.course.id, "rating": 6})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
