from django.db import models
from .hilo_foro import ForumThread
from .usuario import User


class ForumPost(models.Model):
    """Respuesta dentro de un hilo del foro."""
    thread = models.ForeignKey(
        ForumThread,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Hilo'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_posts',
        verbose_name='Autor'
    )
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'foros_mensajes'
        verbose_name = 'Mensaje de foro'
        verbose_name_plural = 'Mensajes de foro'
        ordering = ['created_at']

    def __str__(self):
        return f'Respuesta de {self.author.username} en {self.thread.title}'
