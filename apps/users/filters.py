import django_filters
from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    """Filtros para el modelo User: búsqueda por rol, nombre, email."""
    role = django_filters.ChoiceFilter(choices=User.Role.choices)
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = ['role', 'is_active']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            username__icontains=value
        ) | queryset.filter(
            email__icontains=value
        ) | queryset.filter(
            first_name__icontains=value
        ) | queryset.filter(
            last_name__icontains=value
        )
