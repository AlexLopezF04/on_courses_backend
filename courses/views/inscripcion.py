from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from email_helper import send_enrollment_email
from courses.filters import EnrollmentFilter
from courses.models import Enrollment
from courses.permissions import IsEnrolledOrAdmin, IsAdminUser
from courses.serializers import EnrollmentSerializer, EnrollmentWriteSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """CRUD de inscripciones. Los estudiantes se inscriben a cursos."""
    queryset = Enrollment.objects.all()
    filterset_class = EnrollmentFilter
    ordering_fields = ['enrolled_at']

    def get_serializer_class(self):
        if self.action in ('create',):
            return EnrollmentWriteSerializer
        return EnrollmentSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve', 'update', 'partial_update'):
            return [IsAuthenticated(), IsEnrolledOrAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save(user=self.request.user)
        send_enrollment_email(self.request.user, enrollment.course)
        read_serializer = EnrollmentSerializer(enrollment)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
