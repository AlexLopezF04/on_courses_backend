from django.db import models
from apps.users.models import User


class Category(models.Model):
    """Clasificación de cursos (ej: Frontend, Backend, Data Science)."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    slug = models.SlugField(max_length=120, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Course(models.Model):
    """Curso de tecnología creado por un profesor."""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name='Categoría'
    )
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Profesor'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Precio'
    )
    cover_image = models.URLField(blank=True, verbose_name='Imagen de portada')
    slug = models.SlugField(max_length=280, unique=True, verbose_name='Slug')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.title


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


class Lesson(models.Model):
    """Unidad mínima de aprendizaje. Contiene video y contenido teórico."""
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Módulo'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    content_text = models.TextField(blank=True, verbose_name='Contenido teórico')
    video_url = models.URLField(blank=True, verbose_name='URL del video')
    duration_seconds = models.PositiveIntegerField(
        default=0,
        verbose_name='Duración (segundos)'
    )
    order = models.PositiveIntegerField(verbose_name='Orden')
    completion_percentage = models.PositiveIntegerField(
        default=90,
        verbose_name='% para completar',
        help_text='Porcentaje de avance necesario para considerar la lección completada'
    )

    class Meta:
        db_table = 'lecciones'
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f'{self.module.title} - {self.title}'


class Resource(models.Model):
    """Material descargable asociado a una lección."""
    class Type(models.TextChoices):
        PDF = 'pdf', 'PDF'
        VIDEO = 'video', 'Video'
        CODE = 'code', 'Código'
        LINK = 'link', 'Enlace'
        OTHER = 'other', 'Otro'

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name='Lección'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    file_url = models.URLField(verbose_name='URL del archivo')
    resource_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.OTHER,
        verbose_name='Tipo de recurso'
    )

    class Meta:
        db_table = 'recursos'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.title
