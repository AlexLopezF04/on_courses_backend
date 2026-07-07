from django.db import models

from .leccion import Lesson


class Resource(models.Model):
    """Material descargable asociado a una lección."""

    class Type(models.TextChoices):
        PDF = "pdf", "PDF"
        VIDEO = "video", "Video"
        CODE = "code", "Código"
        LINK = "link", "Enlace"
        OTHER = "other", "Otro"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="resources", verbose_name="Lección"
    )
    title = models.CharField(max_length=255, verbose_name="Título")
    file = models.FileField(upload_to="resources/", blank=True, null=True, verbose_name="Archivo")
    resource_type = models.CharField(
        max_length=20, choices=Type.choices, default=Type.OTHER, verbose_name="Tipo de recurso"
    )

    class Meta:
        db_table = "recursos"
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"

    def __str__(self):
        return self.title
