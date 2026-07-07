import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status

from helpers import create_user, create_professor, create_admin, auth_client, unauth_client
from courses.tests.helpers import create_category, create_course


class CoursePermissionTests(TestCase):
    """Pruebas de permisos sobre cursos."""

    def setUp(self):
        self.student = create_user("frank")
        self.prof = create_professor()
        self.admin = create_admin()
        self.cat = create_category()
        self.course = create_course(category=self.cat, professor=self.prof)

    def test_anyone_can_list_courses(self):
        resp = unauth_client().get("/api/courses/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_student_cannot_create_course(self):
        resp = auth_client(self.student).post(
            "/api/courses/",
            {"category": self.cat.id, "title": "Test", "slug": "test", "price": "10.00"},
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_professor_can_create_course(self):
        resp = auth_client(self.prof).post(
            "/api/courses/",
            {
                "category": self.cat.id,
                "title": "Python Avanzado",
                "slug": "python-avanzado",
                "price": "79.00",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_professor_can_update_own_course(self):
        resp = auth_client(self.prof).patch(
            f"/api/courses/{self.course.id}/", {"title": "Nuevo Título"}
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "Nuevo Título")

    def test_professor_cannot_update_other_course(self):
        other_prof = create_professor("other")
        resp = auth_client(other_prof).patch(
            f"/api/courses/{self.course.id}/", {"title": "Hackeado"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_course(self):
        resp = auth_client(self.admin).delete(f"/api/courses/{self.course.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class CourseFilterTests(TestCase):
    """Pruebas de filtros en cursos."""

    def setUp(self):
        self.client = unauth_client()
        cat = create_category()
        prof = create_professor()
        create_course(cat, prof, "Laravel", price=20, slug="laravel")
        create_course(cat, prof, "Django", price=100, slug="django")

    def test_search_by_title(self):
        resp = self.client.get("/api/courses/?search=lara")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["results"]), 1)

    def test_filter_by_min_price(self):
        resp = self.client.get("/api/courses/?min_price=50")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        names = [c["title"] for c in resp.data["results"]]
        self.assertIn("Django", names)
        self.assertNotIn("Laravel", names)


class FileUploadTests(TestCase):
    """Pruebas de subida de archivos."""

    def setUp(self):
        self.prof = create_professor()
        self.client = auth_client(self.prof)
        cat = create_category()
        self.course = create_course(cat, self.prof, slug="upload-test")

    def _generate_image(self):
        """Genera una imagen PNG en memoria para pruebas."""
        img = Image.new("RGB", (100, 100), color="red")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return SimpleUploadedFile("test.png", buf.read(), content_type="image/png")

    def test_upload_course_cover(self):
        """Sube una imagen de portada a un curso."""
        image = self._generate_image()
        resp = self.client.patch(
            f"/api/courses/{self.course.id}/", {"cover_image": image}, format="multipart"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("/media/", resp.data["cover_image"])
