from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from courses.models import Exam, ExamQuestion, QuestionBank

from .pregunta import QuestionBankSerializer


class ExamSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = "__all__"

    @extend_schema_field(serializers.IntegerField())
    def get_questions_count(self, obj):
        return obj.exam_questions.count()


class ExamDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado que incluye las preguntas con sus opciones."""

    questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = "__all__"

    @extend_schema_field(serializers.ListField())
    def get_questions(self, obj):
        questions = QuestionBank.objects.filter(exam_questions__exam=obj).prefetch_related(
            "options"
        )
        return QuestionBankSerializer(questions, many=True).data


class ExamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            "course",
            "module",
            "title",
            "description",
            "max_attempts",
            "min_score",
            "start_date",
            "end_date",
        ]


class ExamQuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source="question.question_text", read_only=True)

    class Meta:
        model = ExamQuestion
        fields = "__all__"
