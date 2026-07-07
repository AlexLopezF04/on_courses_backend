from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.filters import CertificateFilter
from courses.models import Certificate
from courses.permissions import IsAdminUser, IsEnrolledOrAdmin
from courses.serializers import CertificateSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    """Consulta de certificados. Solo lectura para estudiantes."""

    queryset = Certificate.objects.all()
    filterset_class = CertificateFilter
    search_fields = ["verification_code"]

    def get_serializer_class(self):
        return CertificateSerializer

    def get_permissions(self):
        if self.action in ("list",):
            return [IsAdminUser()]
        return [IsAuthenticated(), IsEnrolledOrAdmin()]
