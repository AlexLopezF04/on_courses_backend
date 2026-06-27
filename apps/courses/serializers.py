from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from apps.courses.models import Category, Course, Module, Lesson, Resource


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        exclude = ['course']


class LessonSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        exclude = ['module']


class LessonDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye los recursos."""
    resources = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listar cursos."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)
    modules_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'price', 'cover_image',
            'category_name', 'professor_name', 'is_active',
            'modules_count', 'created_at'
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_modules_count(self, obj):
        return obj.modules.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye módulos y lecciones."""
    category = CategorySerializer(read_only=True)
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseWriteSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar cursos."""
    class Meta:
        model = Course
        fields = [
            'category', 'title', 'description', 'price',
            'cover_image', 'slug', 'is_active'
        ]
