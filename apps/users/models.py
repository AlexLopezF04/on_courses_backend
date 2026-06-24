from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario personalizado para on_courses.
    AbstractUser ya incluye: username, password, email, first_name, last_name,
    is_active, is_staff, is_superuser, date_joined, last_login.

    Roles del sistema:
        - Estudiante: consume cursos, participa en foros, rinde exámenes.
        - Profesor: crea y gestiona contenido académico.
        - Administrador: control total del sistema.
    """
    class Role(models.TextChoices):
        STUDENT = 'student', 'Estudiante'
        PROFESSOR = 'professor', 'Profesor'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='Rol del usuario'
    )

    # Datos de contacto
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'
