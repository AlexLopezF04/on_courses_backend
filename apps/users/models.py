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
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'


class StudentProfile(models.Model):
    """Información adicional del estudiante. One-to-One con User."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Usuario'
    )
    biography = models.TextField(blank=True, verbose_name='Biografía')
    country = models.CharField(max_length=100, blank=True, verbose_name='País')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    avatar_url = models.URLField(blank=True, verbose_name='URL del avatar')

    class Meta:
        db_table = 'perfiles_estudiante'
        verbose_name = 'Perfil de Estudiante'
        verbose_name_plural = 'Perfiles de Estudiantes'

    def __str__(self):
        return f'Perfil de {self.user.username}'


class ProfessorProfile(models.Model):
    """Información adicional del profesor. One-to-One con User."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professor_profile',
        verbose_name='Usuario'
    )
    professional_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Título profesional'
    )
    specialty = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Especialidad'
    )
    biography = models.TextField(blank=True, verbose_name='Biografía')
    linkedin_url = models.URLField(blank=True, verbose_name='URL de LinkedIn')

    class Meta:
        db_table = 'perfiles_profesor'
        verbose_name = 'Perfil de Profesor'
        verbose_name_plural = 'Perfiles de Profesores'

    def __str__(self):
        return f'Perfil de {self.user.username}'


class AccessLog(models.Model):
    """Registro de inicio/cierre de sesión para auditoría."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='access_logs',
        verbose_name='Usuario'
    )
    ip_address = models.GenericIPAddressField(verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User-Agent')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='Inicio de sesión')
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name='Cierre de sesión')

    class Meta:
        db_table = 'sesiones_acceso'
        verbose_name = 'Sesión de Acceso'
        verbose_name_plural = 'Sesiones de Acceso'

    def __str__(self):
        return f'{self.user.username} - {self.login_time}'
