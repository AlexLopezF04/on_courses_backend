from django.contrib import admin
from apps.progress.models import (
    Enrollment, LessonProgress, QuestionBank, QuestionOption,
    Exam, ExamQuestion, ExamAttempt, AttemptAnswer, Certificate
)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_active', 'total_progress', 'enrolled_at')
    list_filter = ('is_active',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'percentage', 'is_completed', 'updated_at')


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'author', 'question_type')
    list_filter = ('question_type', 'course')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_text', 'is_correct')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'max_attempts', 'min_score')


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'score')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('exam', 'user', 'score', 'is_passed', 'start_time')


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'verification_code', 'issued_at')
    readonly_fields = ('verification_code',)
