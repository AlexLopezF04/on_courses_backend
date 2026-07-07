from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from courses.models import (
    Achievement,
    Announcement,
    Cart,
    CartItem,
    Category,
    Certificate,
    Coupon,
    Course,
    Enrollment,
    Exam,
    ExamAttempt,
    ExamQuestion,
    ForumPost,
    ForumThread,
    Lesson,
    LessonComment,
    LessonProgress,
    Module,
    Order,
    OrderItem,
    QuestionBank,
    Resource,
    Review,
    SupportTicket,
    User,
    UserAchievement,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Panel de administración para usuarios."""

    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("role", "phone")}),
        (
            "Perfil",
            {
                "fields": (
                    "biography",
                    "country",
                    "birth_date",
                    "avatar",
                    "professional_title",
                    "specialty",
                    "linkedin_url",
                )
            },
        ),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "professor", "category", "price", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "professor__username")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "duration_seconds")
    list_filter = ("module__course",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "resource_type")


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "author", "created_at")
    list_filter = ("course",)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ("thread", "author", "created_at")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "author", "created_at")
    list_filter = ("course",)


@admin.register(LessonComment)
class LessonCommentAdmin(admin.ModelAdmin):
    list_display = ("lesson", "author", "parent", "created_at")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "is_active", "total_progress", "enrolled_at")
    list_filter = ("is_active",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "percentage", "is_completed", "updated_at")


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "author", "question_type")
    list_filter = ("question_type", "course")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "max_attempts", "min_score")


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "question", "score")


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ("exam", "user", "score", "is_passed", "start_time")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "verification_code", "issued_at")
    readonly_fields = ("verification_code",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "criteria")
    search_fields = ("name",)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "earned_at")
    list_filter = ("achievement",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "rating", "created_at")
    list_filter = ("rating", "course")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "course", "added_at")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "is_active",
        "current_uses",
        "max_uses",
    )
    list_filter = ("is_active", "discount_type")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created_at")
    list_filter = ("status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "course", "unit_price")


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "status", "created_at")
    list_filter = ("status",)
