from django.db import models

from .modulo import Module


class Lesson(models.Model):
    """Unidad mínima de aprendizaje. Contiene video y contenido teórico."""

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="Módulo"
    )
    title = models.CharField(max_length=255, verbose_name="Título")
    content_text = models.TextField(blank=True, verbose_name="Contenido teórico")
    video_url = models.URLField(blank=True, verbose_name="URL del video")
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name="Duración (segundos)")
    order = models.PositiveIntegerField(verbose_name="Orden")
    completion_percentage = models.PositiveIntegerField(
        default=90,
        verbose_name="% para completar",
        help_text="Porcentaje de avance necesario para considerar la lección completada",
    )

    class Meta:
        db_table = "lecciones"
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ["order"]
        unique_together = ["module", "order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"
