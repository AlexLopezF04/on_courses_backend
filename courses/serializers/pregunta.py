from rest_framework import serializers
from courses.models import QuestionBank


class QuestionBankSerializer(serializers.ModelSerializer):
    """Serializer de lectura para el banco de preguntas. Incluye opciones como JSON."""
    class Meta:
        model = QuestionBank
        fields = '__all__'


class QuestionBankWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = ['course', 'question_text', 'question_type', 'options']
