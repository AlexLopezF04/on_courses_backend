from rest_framework import serializers

from apps.gamification.models import Achievement, Review, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)

    class Meta:
        model = UserAchievement
        fields = '__all__'


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

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('La puntuación debe estar entre 1 y 5')
        return value

    def validate(self, data):
        user = self.context['request'].user
        course = data.get('course')
        if course and Review.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError(
                'Ya has calificado este curso anteriormente'
            )
        return data
