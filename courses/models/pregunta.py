from django.db import models

from .curso import Course
from .usuario import User


class QuestionBank(models.Model):
    """Banco de preguntas creado por el profesor para sus cursos."""

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = "multiple", "Opción múltiple"
        TRUE_FALSE = "true_false", "Verdadero/Falso"
        SINGLE_CHOICE = "single", "Única respuesta"

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="questions", verbose_name="Curso"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="questions", verbose_name="Autor (profesor)"
    )
    question_text = models.TextField(verbose_name="Enunciado de la pregunta")
    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,
        verbose_name="Tipo de pregunta",
    )
    options = models.JSONField(
        default=list,
        verbose_name="Opciones de respuesta",
        help_text='Lista de objetos: [{"text": "...", "is_correct": true/false}]',
    )

    class Meta:
        db_table = "banco_preguntas"
        verbose_name = "Pregunta"
        verbose_name_plural = "Banco de preguntas"

    def __str__(self):
        return self.question_text[:60]
