from django.db import models
from apps.users.models import User
from apps.courses.models import Course, Lesson


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


class Announcement(models.Model):
    """Anuncio del profesor para los alumnos de su curso."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name='Curso'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name='Autor (profesor)'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')

    class Meta:
        db_table = 'anuncios'
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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
