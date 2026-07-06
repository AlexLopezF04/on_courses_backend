from rest_framework import serializers
from courses.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['course', 'rating', 'comment']

    def validate_course(self, value):
        user = self.context['request'].user
        if Review.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError('Ya has valorado este curso')
        return value
