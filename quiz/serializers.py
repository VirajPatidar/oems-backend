from rest_framework import serializers
from .models import *

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

class GetQuizSerializer(serializers.ModelSerializer):

    quiz_status = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiz_status(self, obj):
        return obj.quiz_status()

class QuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        exclude = ['correct_option_number', 'quiz_id']

class QuizQuestionSerializer(serializers.ModelSerializer):

    questions = QuestSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'class_id', 'number_of_questions', 'marks', 'response_released', 'quiz_status', 'start_time', 'end_time', 'questions']