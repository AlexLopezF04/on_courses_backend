from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .curso import Course
from .usuario import User


class Review(models.Model):
    """Valoración y reseña de un curso por parte de un estudiante."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Estudiante"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="reviews", verbose_name="Curso"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Puntuación (1-5)"
    )
    comment = models.TextField(blank=True, verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = "resenas"
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}: {self.rating}/5"
