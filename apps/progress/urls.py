from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.progress.views import (
    EnrollmentViewSet, LessonProgressViewSet,
    QuestionBankViewSet, QuestionOptionViewSet,
    ExamViewSet, ExamQuestionViewSet,
    ExamAttemptViewSet, CertificateViewSet
)

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'lesson-progress', LessonProgressViewSet)
router.register(r'questions', QuestionBankViewSet)
router.register(r'question-options', QuestionOptionViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-questions', ExamQuestionViewSet)
router.register(r'exam-attempts', ExamAttemptViewSet)
router.register(r'certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
