from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from courses.models import LessonComment


class LessonCommentSerializer(serializers.ModelSerializer):
    """Serializer para comentarios con respuestas anidadas."""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = LessonComment
        fields = '__all__'

    @extend_schema_field(serializers.ListField())
    def get_replies(self, obj):
        if obj.replies.exists():
            return LessonCommentSerializer(obj.replies.all(), many=True).data
        return []


class LessonCommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonComment
        fields = ['lesson', 'parent', 'content']
