from rest_framework import serializers

from courses.models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    """Serializer de lectura. Los mensajes vienen como JSONField."""

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = SupportTicket
        fields = "__all__"


class SupportTicketWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ["subject", "description"]
