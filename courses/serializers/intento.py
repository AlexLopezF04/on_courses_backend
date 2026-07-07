from rest_framework import serializers

from courses.models import ExamAttempt


class ExamAttemptSerializer(serializers.ModelSerializer):
    """Serializer de lectura. Las respuestas vienen como JSONField."""

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = ExamAttempt
        fields = "__all__"


class ExamAttemptWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        fields = ["exam"]
