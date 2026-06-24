import django_filters
from apps.courses.models import Course, Module, Lesson


class CourseFilter(django_filters.FilterSet):
    """Filtros para cursos: por categoría, profesor, precio, búsqueda."""
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['category', 'professor', 'is_active']


class ModuleFilter(django_filters.FilterSet):
    class Meta:
        model = Module
        fields = ['course']


class LessonFilter(django_filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ['module']
