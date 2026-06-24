from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.courses.views import (
    CategoryViewSet, CourseViewSet, ModuleViewSet,
    LessonViewSet, ResourceViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
