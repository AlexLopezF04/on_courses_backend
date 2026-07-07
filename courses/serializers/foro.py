from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from courses.models import ForumPost, ForumThread


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)

    class Meta:
        model = ForumPost
        fields = "__all__"


class ForumThreadSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumThread
        fields = "__all__"

    @extend_schema_field(serializers.IntegerField())
    def get_posts_count(self, obj):
        return obj.posts.count()


class ForumThreadDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye los mensajes del hilo."""

    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    posts = ForumPostSerializer(many=True, read_only=True)

    class Meta:
        model = ForumThread
        fields = "__all__"


class ForumThreadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumThread
        fields = ["course", "title", "content"]


class ForumPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ["thread", "content"]
