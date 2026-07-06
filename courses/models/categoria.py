from django.db import models


class Category(models.Model):
    """Clasificación de cursos (ej: Frontend, Backend, Data Science)."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    slug = models.SlugField(max_length=120, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name
