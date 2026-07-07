from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import QuestionBankFilter
from courses.models import QuestionBank
from courses.permissions import IsProfessorOrAdmin
from courses.serializers import (
    QuestionBankSerializer,
    QuestionBankWriteSerializer,
)


class QuestionBankViewSet(viewsets.ModelViewSet):
    """CRUD del banco de preguntas."""

    queryset = QuestionBank.objects.all()
    filterset_class = QuestionBankFilter
    search_fields = ["question_text"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return QuestionBankWriteSerializer
        return QuestionBankSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsProfessorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
