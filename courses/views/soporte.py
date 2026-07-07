from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.filters import SupportTicketFilter
from courses.models import SupportTicket
from courses.permissions import IsAdminUser, IsOwnerOfTicket
from courses.serializers import (
    SupportTicketSerializer,
    SupportTicketWriteSerializer,
)


class SupportTicketViewSet(viewsets.ModelViewSet):
    """CRUD de tickets de soporte."""

    queryset = SupportTicket.objects.all()
    filterset_class = SupportTicketFilter
    search_fields = ["subject", "description"]

    def get_serializer_class(self):
        if self.action in ("create",):
            return SupportTicketWriteSerializer
        return SupportTicketSerializer

    def get_permissions(self):
        if self.action in ("list",):
            return [IsAdminUser()]
        if self.action in ("retrieve", "update", "partial_update"):
            return [IsAuthenticated(), IsOwnerOfTicket()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """Agrega un mensaje al JSONField messages del ticket."""
        ticket = self.get_object()
        message_text = request.data.get("message", "")
        if not message_text:
            return Response(
                {"error": "El mensaje no puede estar vacío"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_message = {
            "sender_id": request.user.id,
            "sender_name": request.user.get_full_name() or request.user.username,
            "message": message_text,
            "sent_at": now().isoformat(),
        }
        ticket.messages.append(new_message)
        ticket.save(update_fields=["messages", "updated_at"])
        return Response(new_message, status=status.HTTP_201_CREATED)
