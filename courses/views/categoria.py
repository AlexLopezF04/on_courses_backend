from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from courses.models import Category
from courses.permissions import IsAdminUser
from courses.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD de categorías. Lectura pública, escritura solo admin."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdminUser()]
