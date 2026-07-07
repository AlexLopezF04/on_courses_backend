import django_filters

from courses.models import (
    Announcement,
    Certificate,
    Course,
    Enrollment,
    Exam,
    ExamAttempt,
    ForumThread,
    Lesson,
    LessonComment,
    LessonProgress,
    Module,
    Order,
    QuestionBank,
    Review,
    SupportTicket,
    User,
    UserAchievement,
)


class UserFilter(django_filters.FilterSet):
    """Filtros para el modelo User: búsqueda por rol, nombre, email."""

    role = django_filters.ChoiceFilter(choices=User.Role.choices)
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = User
        fields = ["role", "is_active"]

    def filter_search(self, queryset, name, value):
        return (
            queryset.filter(username__icontains=value)
            | queryset.filter(email__icontains=value)
            | queryset.filter(first_name__icontains=value)
            | queryset.filter(last_name__icontains=value)
        )


class CourseFilter(django_filters.FilterSet):
    """Filtros para cursos: por categoría, profesor, precio, búsqueda."""

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Course
        fields = ["category", "professor", "is_active"]


class ModuleFilter(django_filters.FilterSet):
    class Meta:
        model = Module
        fields = ["course"]


class LessonFilter(django_filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ["module"]


class ForumThreadFilter(django_filters.FilterSet):
    class Meta:
        model = ForumThread
        fields = ["course", "author"]


class AnnouncementFilter(django_filters.FilterSet):
    class Meta:
        model = Announcement
        fields = ["course", "author"]


class LessonCommentFilter(django_filters.FilterSet):
    class Meta:
        model = LessonComment
        fields = ["lesson", "author", "parent"]


class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = ["user", "course", "is_active"]


class LessonProgressFilter(django_filters.FilterSet):
    class Meta:
        model = LessonProgress
        fields = ["user", "lesson", "is_completed"]


class QuestionBankFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionBank
        fields = ["course", "author", "question_type"]


class ExamFilter(django_filters.FilterSet):
    class Meta:
        model = Exam
        fields = ["course", "module"]


class ExamAttemptFilter(django_filters.FilterSet):
    class Meta:
        model = ExamAttempt
        fields = ["exam", "user", "is_passed"]


class CertificateFilter(django_filters.FilterSet):
    class Meta:
        model = Certificate
        fields = ["user", "course"]


class UserAchievementFilter(django_filters.FilterSet):
    class Meta:
        model = UserAchievement
        fields = ["user", "achievement"]


class ReviewFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")

    class Meta:
        model = Review
        fields = ["user", "course", "rating"]


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ["user", "status", "coupon"]


class SupportTicketFilter(django_filters.FilterSet):
    class Meta:
        model = SupportTicket
        fields = ["user", "status"]
