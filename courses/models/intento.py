from django.db import models

from .examen import Exam
from .usuario import User


class ExamAttempt(models.Model):
    """Intento de un estudiante en una evaluación."""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="attempts", verbose_name="Evaluación"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="exam_attempts", verbose_name="Estudiante"
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Inicio del intento")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Fin del intento")
    score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Nota obtenida"
    )
    is_passed = models.BooleanField(default=False, verbose_name="¿Aprobado?")
    answers = models.JSONField(
        default=list,
        verbose_name="Respuestas del intento",
        help_text='Lista: [{"question_id": 1, "option_index": 0, "is_correct": true}]',
    )

    class Meta:
        db_table = "intentos_evaluacion"
        verbose_name = "Intento de evaluación"
        verbose_name_plural = "Intentos de evaluación"

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} (intento {self.id})"
