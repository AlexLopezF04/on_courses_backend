import django_filters

from apps.progress.models import (
    Certificate,
    Enrollment,
    Exam,
    ExamAttempt,
    LessonProgress,
    QuestionBank,
)


class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = ['user', 'course', 'is_active']


class LessonProgressFilter(django_filters.FilterSet):
    class Meta:
        model = LessonProgress
        fields = ['user', 'lesson', 'is_completed']


class QuestionBankFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionBank
        fields = ['course', 'author', 'question_type']


class ExamFilter(django_filters.FilterSet):
    class Meta:
        model = Exam
        fields = ['course', 'module']


class ExamAttemptFilter(django_filters.FilterSet):
    class Meta:
        model = ExamAttempt
        fields = ['exam', 'user', 'is_passed']


class CertificateFilter(django_filters.FilterSet):
    class Meta:
        model = Certificate
        fields = ['user', 'course']
