from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.filters import ExamAttemptFilter
from courses.models import (
    Certificate,
    ExamAttempt,
    ExamQuestion,
    QuestionBank,
)
from courses.permissions import IsAdminUser, IsEnrolledOrAdmin
from courses.serializers import ExamAttemptSerializer, ExamAttemptWriteSerializer


class ExamAttemptViewSet(viewsets.ModelViewSet):
    """
    Intentos de evaluación. Al enviar las respuestas, calcula la nota
    y genera certificado si corresponde.
    """

    queryset = ExamAttempt.objects.all()
    filterset_class = ExamAttemptFilter
    ordering_fields = ["start_time"]

    def get_serializer_class(self):
        if self.action in ("create",):
            return ExamAttemptWriteSerializer
        return ExamAttemptSerializer

    def get_permissions(self):
        if self.action in ("list",):
            return [IsAdminUser()]
        if self.action in ("retrieve",):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """
        Envía las respuestas del intento, calcula la nota y genera
        certificado si la nota mínima es alcanzada.

        Body esperado:
            {"answers": [{"question_id": 1, "option_index": 0}, ...]}
        """
        attempt = self.get_object()
        if attempt.end_time:
            return Response(
                {"error": "Este intento ya fue enviado"}, status=status.HTTP_400_BAD_REQUEST
            )

        answers_data = request.data.get("answers", [])
        total_score = 0
        exam_questions = ExamQuestion.objects.filter(exam=attempt.exam).select_related("question")
        max_score = sum(eq.score for eq in exam_questions)

        saved_answers = []
        for ans_data in answers_data:
            question_id = ans_data.get("question_id")
            option_index = ans_data.get("option_index")

            try:
                question = QuestionBank.objects.get(id=question_id)
                options = question.options
                if not isinstance(options, list) or option_index is None:
                    continue
                if option_index < 0 or option_index >= len(options):
                    continue
                selected = options[option_index]
                is_correct = selected.get("is_correct", False)
            except QuestionBank.DoesNotExist:
                continue

            saved_answers.append(
                {
                    "question_id": question_id,
                    "option_index": option_index,
                    "option_text": selected.get("text", ""),
                    "is_correct": is_correct,
                }
            )

            if is_correct:
                eq = exam_questions.filter(question_id=question_id).first()
                if eq:
                    total_score += eq.score

        # Calcula nota final en porcentaje
        score_percent = (total_score / max_score * 100) if max_score > 0 else 0
        attempt.score = round(score_percent, 2)
        attempt.is_passed = score_percent >= attempt.exam.min_score
        attempt.end_time = now()
        attempt.answers = saved_answers
        attempt.save()

        # Si aprobó, genera certificado automático
        if attempt.is_passed:
            Certificate.objects.get_or_create(user=attempt.user, course=attempt.exam.course)

        return Response(ExamAttemptSerializer(attempt).data)
