from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.progress.models import (
    AttemptAnswer,
    Certificate,
    Enrollment,
    Exam,
    ExamAttempt,
    ExamQuestion,
    LessonProgress,
    QuestionBank,
    QuestionOption,
)


class EnrollmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'


class EnrollmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course']

    def validate_course(self, value):
        user = self.context['request'].user
        if Enrollment.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError('Ya estás inscrito en este curso')
        return value


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = '__all__'


class LessonProgressWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['lesson', 'percentage', 'last_video_position', 'is_completed']


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionBankSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionBank
        fields = '__all__'


class QuestionBankWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = ['course', 'question_text', 'question_type']


class ExamSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    @extend_schema_field(serializers.IntegerField())
    def get_questions_count(self, obj):
        return obj.exam_questions.count()


class ExamDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye las preguntas con sus opciones."""
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    @extend_schema_field(serializers.ListField())
    def get_questions(self, obj):
        questions = QuestionBank.objects.filter(
            exam_questions__exam=obj
        ).prefetch_related('options')
        return QuestionBankSerializer(questions, many=True).data


class ExamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'course', 'module', 'title', 'description',
            'max_attempts', 'min_score', 'start_date', 'end_date'
        ]


class ExamQuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)

    class Meta:
        model = ExamQuestion
        fields = '__all__'


class AttemptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptAnswer
        fields = '__all__'


class ExamAttemptSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    answers = AttemptAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ExamAttempt
        fields = '__all__'


class ExamAttemptWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        fields = ['exam']


class CertificateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = '__all__'
