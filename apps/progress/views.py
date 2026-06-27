from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.email_helper import send_enrollment_email
from apps.progress.filters import (
    CertificateFilter,
    EnrollmentFilter,
    ExamAttemptFilter,
    ExamFilter,
    LessonProgressFilter,
    QuestionBankFilter,
)
from apps.progress.models import (
    AttemptAnswer,
    Certificate,
    Enrollment,
    Exam,
    ExamAttempt,
    ExamQuestion,
    LessonProgress,
    QuestionBank,
    QuestionOption,
)
from apps.progress.permissions import IsEnrolledOrAdmin
from apps.progress.serializers import (
    CertificateSerializer,
    EnrollmentSerializer,
    EnrollmentWriteSerializer,
    ExamAttemptSerializer,
    ExamAttemptWriteSerializer,
    ExamDetailSerializer,
    ExamQuestionSerializer,
    ExamSerializer,
    ExamWriteSerializer,
    LessonProgressSerializer,
    LessonProgressWriteSerializer,
    QuestionBankSerializer,
    QuestionBankWriteSerializer,
    QuestionOptionSerializer,
)
from apps.users.permissions import IsAdminUser, IsProfessorOrAdmin


class EnrollmentViewSet(viewsets.ModelViewSet):
    """CRUD de inscripciones. Los estudiantes se inscriben a cursos."""
    queryset = Enrollment.objects.all()
    filterset_class = EnrollmentFilter
    ordering_fields = ['enrolled_at']

    def get_serializer_class(self):
        if self.action in ('create',):
            return EnrollmentWriteSerializer
        return EnrollmentSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve', 'update', 'partial_update'):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save(user=self.request.user)
        send_enrollment_email(self.request.user, enrollment.course)
        read_serializer = EnrollmentSerializer(enrollment)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class LessonProgressViewSet(viewsets.ModelViewSet):
    """CRUD de progreso de lecciones. Sincroniza avance de video."""
    queryset = LessonProgress.objects.all()
    filterset_class = LessonProgressFilter
    ordering_fields = ['updated_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return LessonProgressWriteSerializer
        return LessonProgressSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve',):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionOptionViewSet(viewsets.ModelViewSet):
    """CRUD de opciones de respuesta."""
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]


class QuestionBankViewSet(viewsets.ModelViewSet):
    """CRUD del banco de preguntas."""
    queryset = QuestionBank.objects.all()
    filterset_class = QuestionBankFilter
    search_fields = ['question_text']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return QuestionBankWriteSerializer
        return QuestionBankSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ExamViewSet(viewsets.ModelViewSet):
    """CRUD de evaluaciones."""
    queryset = Exam.objects.all()
    filterset_class = ExamFilter
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ExamWriteSerializer
        return ExamSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]


class ExamQuestionViewSet(viewsets.ModelViewSet):
    """Asignación de preguntas a evaluaciones."""
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    ordering_fields = ['score']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]


class ExamAttemptViewSet(viewsets.ModelViewSet):
    """
    Intentos de evaluación. Al enviar las respuestas, calcula la nota
    y genera certificado si corresponde.
    """
    queryset = ExamAttempt.objects.all()
    filterset_class = ExamAttemptFilter
    ordering_fields = ['start_time']

    def get_serializer_class(self):
        if self.action in ('create',):
            return ExamAttemptWriteSerializer
        return ExamAttemptSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve',):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Envía las respuestas del intento, calcula la nota y genera
        certificado si la nota mínima es alcanzada.
        """
        attempt = self.get_object()
        if attempt.end_time:
            return Response(
                {'error': 'Este intento ya fue enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        answers_data = request.data.get('answers', [])
        total_score = 0
        exam_questions = ExamQuestion.objects.filter(exam=attempt.exam)
        max_score = sum(eq.score for eq in exam_questions)

        for ans_data in answers_data:
            question_id = ans_data.get('question')
            option_id = ans_data.get('selected_option')

            try:
                question = QuestionBank.objects.get(id=question_id)
                option = QuestionOption.objects.get(id=option_id, question=question)
            except (QuestionBank.DoesNotExist, QuestionOption.DoesNotExist):
                continue

            is_correct = option.is_correct
            AttemptAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=option,
                is_correct=is_correct
            )
            if is_correct:
                eq = exam_questions.filter(question=question).first()
                if eq:
                    total_score += eq.score

        # Calcula nota final en porcentaje
        score_percent = (total_score / max_score * 100) if max_score > 0 else 0
        attempt.score = round(score_percent, 2)
        attempt.is_passed = score_percent >= attempt.exam.min_score
        attempt.end_time = now()
        attempt.save()

        # Si aprobó, genera certificado automático
        if attempt.is_passed:
            Certificate.objects.get_or_create(
                user=attempt.user,
                course=attempt.exam.course
            )

        return Response(ExamAttemptSerializer(attempt).data)


class CertificateViewSet(viewsets.ModelViewSet):
    """Consulta de certificados. Solo lectura para estudiantes."""
    queryset = Certificate.objects.all()
    filterset_class = CertificateFilter
    search_fields = ['verification_code']

    def get_serializer_class(self):
        return CertificateSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        return [IsAuthenticated(), IsEnrolledOrAdmin()]
