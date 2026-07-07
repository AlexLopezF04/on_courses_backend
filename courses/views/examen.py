from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import ExamFilter
from courses.models import Exam, ExamQuestion
from courses.permissions import IsProfessorOrAdmin
from courses.serializers import (
    ExamDetailSerializer,
    ExamQuestionSerializer,
    ExamSerializer,
    ExamWriteSerializer,
)


class ExamViewSet(viewsets.ModelViewSet):
    """CRUD de evaluaciones."""

    queryset = Exam.objects.all()
    filterset_class = ExamFilter
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ExamDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return ExamWriteSerializer
        return ExamSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]


class ExamQuestionViewSet(viewsets.ModelViewSet):
    """Asignación de preguntas a evaluaciones."""

    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    ordering_fields = ["score"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]
