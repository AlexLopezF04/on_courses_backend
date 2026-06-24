from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.community.views import (
    ForumThreadViewSet, ForumPostViewSet,
    AnnouncementViewSet, LessonCommentViewSet
)

router = DefaultRouter()
router.register(r'forum-threads', ForumThreadViewSet)
router.register(r'forum-posts', ForumPostViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'lesson-comments', LessonCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
