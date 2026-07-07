from django.db import models

from .categoria import Category
from .usuario import User


class Course(models.Model):
    """Curso de tecnología creado por un profesor."""

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="courses", verbose_name="Categoría"
    )
    professor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses", verbose_name="Profesor"
    )
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio")
    cover_image = models.ImageField(
        upload_to="courses/covers/", blank=True, null=True, verbose_name="Imagen de portada"
    )
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = "cursos"
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
