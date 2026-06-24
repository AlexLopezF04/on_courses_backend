from django.db import models
from apps.users.models import User
from apps.courses.models import Course


class Achievement(models.Model):
    """Definición de un logro que los estudiantes pueden desbloquear."""
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon_url = models.URLField(blank=True, verbose_name='URL del ícono')
    criteria = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Criterio de desbloqueo (ej: completar 5 cursos)'
    )

    class Meta:
        db_table = 'logros'
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Relación muchos a muchos: logros obtenidos por cada usuario."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Usuario'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Logro'
    )
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de obtención')

    class Meta:
        db_table = 'logros_usuarios'
        verbose_name = 'Logro de usuario'
        verbose_name_plural = 'Logros de usuarios'
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f'{self.user.username} → {self.achievement.name}'


class Review(models.Model):
    """Valoración y reseña de un curso por parte de un estudiante."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Estudiante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Curso'
    )
    rating = models.PositiveIntegerField(
        verbose_name='Puntuación (1-5)'
    )
    comment = models.TextField(blank=True, verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'resenas'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}: {self.rating}/5'
