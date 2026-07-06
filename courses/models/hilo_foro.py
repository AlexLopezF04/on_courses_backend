from django.db import models
from .curso import Course
from .usuario import User


class ForumThread(models.Model):
    """Hilo de discusión dentro de un curso."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='forum_threads',
        verbose_name='Curso'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_threads',
        verbose_name='Autor'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'foros_temas'
        verbose_name = 'Tema de foro'
        verbose_name_plural = 'Temas de foro'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
