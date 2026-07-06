from django.db import models
from .curso import Course
from .modulo import Module
from .pregunta import QuestionBank


class Exam(models.Model):
    """Evaluación configurada por el profesor."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='exams',
        verbose_name='Curso'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='exams',
        verbose_name='Módulo (opcional)'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    max_attempts = models.PositiveIntegerField(default=3, verbose_name='Intentos máximos')
    min_score = models.PositiveIntegerField(
        default=80,
        verbose_name='Nota mínima para aprobar (%)'
    )
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de fin')

    class Meta:
        db_table = 'evaluaciones'
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    """Relación muchos a muchos: qué preguntas pertenecen a cada evaluación."""
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_questions',
        verbose_name='Evaluación'
    )
    question = models.ForeignKey(
        QuestionBank,
        on_delete=models.CASCADE,
        related_name='exam_questions',
        verbose_name='Pregunta'
    )
    score = models.PositiveIntegerField(default=10, verbose_name='Puntaje de la pregunta')

    class Meta:
        db_table = 'preguntas_evaluacion'
        verbose_name = 'Pregunta de evaluación'
        verbose_name_plural = 'Preguntas de evaluación'
        unique_together = ['exam', 'question']

    def __str__(self):
        return f'{self.exam.title} - {self.question.question_text[:40]}'
