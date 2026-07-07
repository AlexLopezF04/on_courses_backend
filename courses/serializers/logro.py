from rest_framework import serializers

from courses.models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"


class UserAchievementSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    achievement_name = serializers.CharField(source="achievement.name", read_only=True)

    class Meta:
        model = UserAchievement
        fields = "__all__"
