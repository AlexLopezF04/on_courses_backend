from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.gamification.views import AchievementViewSet, ReviewViewSet, UserAchievementViewSet

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet)
router.register(r'user-achievements', UserAchievementViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
