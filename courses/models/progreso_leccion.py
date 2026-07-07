from django.db import models

from .leccion import Lesson
from .usuario import User


class LessonProgress(models.Model):
    """Progreso individual por lección. Incluye sincronización de video."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lesson_progress", verbose_name="Estudiante"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress", verbose_name="Lección"
    )
    is_completed = models.BooleanField(default=False, verbose_name="Completada")
    percentage = models.PositiveIntegerField(default=0, verbose_name="Porcentaje de avance")
    last_video_position = models.PositiveIntegerField(
        default=0, verbose_name="Última posición del video (segundos)"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        db_table = "progreso_lecciones"
        verbose_name = "Progreso de lección"
        verbose_name_plural = "Progresos de lecciones"
        unique_together = ["user", "lesson"]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}: {self.percentage}%"
