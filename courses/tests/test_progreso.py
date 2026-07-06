from django.core import mail
from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_professor, create_admin, auth_client, unauth_client
from courses.tests.helpers import create_category, create_course
from courses.models import Enrollment


class EnrollmentTests(TestCase):
    """Pruebas de inscripciones."""

    def setUp(self):
        self.student = create_user('helen')
        self.client = auth_client(self.student)
        cat = create_category()
        prof = create_professor()
        self.course = create_course(cat, prof)

    def test_enroll_in_course(self):
        resp = self.client.post('/api/enrollments/', {
            'course': self.course.id
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['user'], self.student.id)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Inscripción confirmada', mail.outbox[0].subject)
        self.assertIn(self.course.title, mail.outbox[0].body)

    def test_double_enrollment_fails(self):
        Enrollment.objects.create(user=self.student, course=self.course)
        resp = self.client.post('/api/enrollments/', {
            'course': self.course.id
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
