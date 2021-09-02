from rest_framework import serializers
from .models import *
from klass.models import Study

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



class TeachQuizQuestionSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'class_id', 'number_of_questions', 'marks', 'response_released', 'quiz_status', 'start_time', 'end_time', 'questions']



class QuizResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizResponse
        fields = '__all__'



class SubmissionStatusSerializer(serializers.ModelSerializer):

    name=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = SubmissionStatus
        fields = ['id', 'name', 'email', 'submission_status', 'marks_scored', 'profile_picture']

    def get_name(self, obj):
        return obj.student_id.name

    def get_email(self, obj):
        return obj.student_id.email

    def get_profile_picture(self, obj):
        return obj.student_id.user.avatar.url



class QuizStatisticsSerializer(serializers.ModelSerializer):

    quiz_submission_status = SubmissionStatusSerializer(many=True, read_only=True)
    total_students=serializers.SerializerMethodField()
    students_submitted=serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'class_id', 'students_submitted', 'total_students', 'number_of_questions', 'marks', 'response_released', 'quiz_status', 'start_time', 'end_time', 'quiz_submission_status']

    def get_total_students(self, obj):
        return len(Study.objects.filter(class_id = obj.class_id))

    def get_students_submitted(self, obj):
        return len(SubmissionStatus.objects.filter(class_id = obj.class_id, quiz_id=obj.id, submission_status=True))