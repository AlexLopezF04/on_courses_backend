from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.gamification.views import (
    AchievementViewSet, UserAchievementViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet)
router.register(r'user-achievements', UserAchievementViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
