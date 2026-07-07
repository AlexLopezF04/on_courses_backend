from rest_framework import serializers

from courses.models import LessonProgress


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)

    class Meta:
        model = LessonProgress
        fields = "__all__"


class LessonProgressWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["lesson", "percentage", "last_video_position", "is_completed"]
