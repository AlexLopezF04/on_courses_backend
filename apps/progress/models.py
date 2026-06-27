import uuid

from django.db import models

from apps.courses.models import Course, Lesson, Module
from apps.users.models import User


class Enrollment(models.Model):
    """Inscripción de un estudiante en un curso."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Estudiante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Curso'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inscripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    total_progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Progreso total (%)'
    )

    class Meta:
        db_table = 'inscripciones'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} → {self.course.title}'


class LessonProgress(models.Model):
    """Progreso individual por lección. Incluye sincronización de video."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name='Estudiante'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Lección'
    )
    is_completed = models.BooleanField(default=False, verbose_name='Completada')
    percentage = models.PositiveIntegerField(default=0, verbose_name='Porcentaje de avance')
    last_video_position = models.PositiveIntegerField(
        default=0,
        verbose_name='Última posición del video (segundos)'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        db_table = 'progreso_lecciones'
        verbose_name = 'Progreso de lección'
        verbose_name_plural = 'Progresos de lecciones'
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title}: {self.percentage}%'


class QuestionBank(models.Model):
    """Banco de preguntas creado por el profesor para sus cursos."""
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple', 'Opción múltiple'
        TRUE_FALSE = 'true_false', 'Verdadero/Falso'
        SINGLE_CHOICE = 'single', 'Única respuesta'

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Curso'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Autor (profesor)'
    )
    question_text = models.TextField(verbose_name='Enunciado de la pregunta')
    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,
        verbose_name='Tipo de pregunta'
    )

    class Meta:
        db_table = 'banco_preguntas'
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Banco de preguntas'

    def __str__(self):
        return self.question_text[:60]


class QuestionOption(models.Model):
    """Opción de respuesta para una pregunta del banco."""
    question = models.ForeignKey(
        QuestionBank,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Pregunta'
    )
    option_text = models.CharField(max_length=255, verbose_name='Texto de la opción')
    is_correct = models.BooleanField(default=False, verbose_name='¿Es correcta?')

    class Meta:
        db_table = 'opciones_pregunta'
        verbose_name = 'Opción de respuesta'
        verbose_name_plural = 'Opciones de respuesta'

    def __str__(self):
        return self.option_text[:50]


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


class ExamAttempt(models.Model):
    """Intento de un estudiante en una evaluación."""
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Evaluación'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='exam_attempts',
        verbose_name='Estudiante'
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Inicio del intento')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Fin del intento')
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Nota obtenida'
    )
    is_passed = models.BooleanField(default=False, verbose_name='¿Aprobado?')

    class Meta:
        db_table = 'intentos_evaluacion'
        verbose_name = 'Intento de evaluación'
        verbose_name_plural = 'Intentos de evaluación'

    def __str__(self):
        return f'{self.user.username} - {self.exam.title} (intento {self.id})'


class AttemptAnswer(models.Model):
    """Respuesta específica a cada pregunta dentro de un intento."""
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Intento'
    )
    question = models.ForeignKey(
        QuestionBank,
        on_delete=models.CASCADE,
        verbose_name='Pregunta'
    )
    selected_option = models.ForeignKey(
        QuestionOption,
        on_delete=models.CASCADE,
        verbose_name='Opción seleccionada'
    )
    is_correct = models.BooleanField(default=False, verbose_name='¿Correcta?')

    class Meta:
        db_table = 'respuestas_intentos'
        verbose_name = 'Respuesta de intento'
        verbose_name_plural = 'Respuestas de intentos'

    def __str__(self):
        return f'{self.attempt.id} - Q{self.question.id}: {"✓" if self.is_correct else "✗"}'


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
