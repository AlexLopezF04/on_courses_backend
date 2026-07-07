from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from courses.views import (
    AchievementViewSet,
    AnnouncementViewSet,
    CartItemViewSet,
    CartViewSet,
    CategoryViewSet,
    CertificateViewSet,
    CouponViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    ExamAttemptViewSet,
    ExamQuestionViewSet,
    ExamViewSet,
    ForumPostViewSet,
    ForumThreadViewSet,
    LessonCommentViewSet,
    LessonProgressViewSet,
    LessonViewSet,
    LogoutView,
    ModuleViewSet,
    OrderViewSet,
    QuestionBankViewSet,
    RegisterView,
    ResourceViewSet,
    ReviewViewSet,
    SupportTicketViewSet,
    UserAchievementViewSet,
    UserViewSet,
    health_check,
)

router = DefaultRouter()
# Users
router.register(r"users", UserViewSet)
# Courses
router.register(r"categories", CategoryViewSet)
# Core Courses
router.register(r"courses", CourseViewSet)
router.register(r"modules", ModuleViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"resources", ResourceViewSet)
# Community
router.register(r"forum-threads", ForumThreadViewSet)
router.register(r"forum-posts", ForumPostViewSet)
router.register(r"announcements", AnnouncementViewSet)
router.register(r"lesson-comments", LessonCommentViewSet)
# Progress
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"lesson-progress", LessonProgressViewSet)
router.register(r"questions", QuestionBankViewSet)
router.register(r"exams", ExamViewSet)
router.register(r"exam-questions", ExamQuestionViewSet)
router.register(r"exam-attempts", ExamAttemptViewSet)
router.register(r"certificates", CertificateViewSet)
# Gamification
router.register(r"achievements", AchievementViewSet)
router.register(r"user-achievements", UserAchievementViewSet)
router.register(r"reviews", ReviewViewSet)
# Commercial
router.register(r"carts", CartViewSet)
router.register(r"cart-items", CartItemViewSet)
router.register(r"coupons", CouponViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"support-tickets", SupportTicketViewSet)

urlpatterns = [
    # Health check
    path("health/", health_check),
    # Autenticación JWT
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    # Endpoints registrados vía router
    path("", include(router.urls)),
]
