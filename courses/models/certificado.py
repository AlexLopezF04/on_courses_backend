import uuid
from django.db import models
from .curso import Course
from .usuario import User


class Certificate(models.Model):
    """Certificado generado automáticamente al aprobar una evaluación final."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='Estudiante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='Curso'
    )
    verification_code = models.CharField(
        max_length=36,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Código de verificación'
    )
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de emisión')

    class Meta:
        db_table = 'certificados'
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'Certificado {self.user.username} - {self.course.title}'
