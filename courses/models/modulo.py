from django.db import models
from .curso import Course


class Module(models.Model):
    """Bloque temático dentro de un curso. Orden secuencial."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Curso'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    order = models.PositiveIntegerField(verbose_name='Orden')

    class Meta:
        db_table = 'modulos'
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'
