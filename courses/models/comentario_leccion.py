from django.db import models
from .leccion import Lesson
from .usuario import User


class LessonComment(models.Model):
    """Comentario en una lección. Soporta respuestas anidadas (autorreferencia)."""
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Lección'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_comments',
        verbose_name='Autor'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Comentario padre'
    )
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'comentarios_lecciones'
        verbose_name = 'Comentario de lección'
        verbose_name_plural = 'Comentarios de lecciones'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} en {self.lesson.title}'
