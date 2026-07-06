from django.db import models
from .curso import Course
from .usuario import User


class Enrollment(models.Model):
    """Inscripción de un estudiante en un curso."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Estudiante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Curso'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inscripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    total_progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Progreso total (%)'
    )

    class Meta:
        db_table = 'inscripciones'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} → {self.course.title}'
