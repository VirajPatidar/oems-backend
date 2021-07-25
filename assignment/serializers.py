from rest_framework import serializers
from datetime import datetime


from .models import *
from klass.models import Study
from .models import SubmissionStatus

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'name', 'due_on']


class GetAssignmentSerializer(serializers.ModelSerializer):

    assignment_status = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_assignment_status(self, obj):
        return obj.assignment_status()

class SubmitAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Response
        fields = '__all__'

class GetAssignmentResponseSerializer(serializers.ModelSerializer):

    submission_status = serializers.SerializerMethodField('get_submission_status')
    marks = serializers.SerializerMethodField('get_marks')

    def get_marks(self, obj):
        if obj.idGraded==True:
            assign_id = obj.assignment_id
            student_id = obj.student_id
            marks_obj = SubmissionStatus.objects.get(student_id=student_id, assignment_id=assign_id)
            print(marks_obj)
            marks = marks_obj.marks_scored
            return str(marks)
        else:
            return "Your Assignment is not yet Graded"


    def get_submission_status(self, obj):
        if obj.assignment_id.due_on > datetime.now(obj.assignment_id.due_on.tzinfo):
            return 'Assignment Submitted Before Due'
        else:
            return 'Assignment Submitted Late'

    class Meta:
        model = Assignment_Response
        fields = ['submission_file', 'submited_data', 'submission_status','marks']


# class GetTeacherAssignmentResponseListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubmissionStatus
#         fields = ['']