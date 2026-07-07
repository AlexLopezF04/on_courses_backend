from rest_framework import serializers

from courses.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye los recursos."""

    resources = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"
