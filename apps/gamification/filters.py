import django_filters

from apps.gamification.models import Review, UserAchievement


class UserAchievementFilter(django_filters.FilterSet):
    class Meta:
        model = UserAchievement
        fields = ['user', 'achievement']


class ReviewFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')

    class Meta:
        model = Review
        fields = ['user', 'course', 'rating']
