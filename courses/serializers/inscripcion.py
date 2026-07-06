from rest_framework import serializers
from courses.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'


class EnrollmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course']

    def validate_course(self, value):
        user = self.context['request'].user
        if Enrollment.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError('Ya estás inscrito en este curso')
        return value
