from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo principal de usuarios de on_courses.
    AbstractUser ya incluye: username, email, password, first_name,
    last_name, is_active, is_staff, is_superuser, date_joined, last_login.

    Roles del sistema:
        - student: consume cursos, participa en foros, rinde exámenes.
        - professor: crea y gestiona contenido académico.
        - admin: control total del sistema.

    Campos de perfil unificados (según rol):
        - Estudiante: biography, country, birth_date, avatar
        - Profesor: professional_title, specialty, biography, linkedin_url
    """
    class Role(models.TextChoices):
        STUDENT = 'student', 'Estudiante'
        PROFESSOR = 'professor', 'Profesor'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='Rol'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')

    # --- Campos de perfil unificados ---
    biography = models.TextField(blank=True, verbose_name='Biografía')
    country = models.CharField(max_length=100, blank=True, verbose_name='País')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    professional_title = models.CharField(
        max_length=200, blank=True, verbose_name='Título profesional'
    )
    specialty = models.CharField(max_length=200, blank=True, verbose_name='Especialidad')
    linkedin_url = models.URLField(blank=True, verbose_name='URL de LinkedIn')

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'
