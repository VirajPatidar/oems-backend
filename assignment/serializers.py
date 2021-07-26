from rest_framework import serializers
from datetime import datetime


from .models import *
from klass.models import Study
from .models import SubmissionStatus, Grade_Assignment

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
        if obj.isGraded==True:
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
        fields = ['submission_file', 'submited_date', 'submission_status','marks']


class GetTeacherAssignmentResponseListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_student_name')
    email = serializers.SerializerMethodField('get_student_email')

    def get_student_name(self, obj):
        return obj.student_id.name
    
    def get_student_email(self, obj):
        return obj.student_id.email

    class Meta:
        model = Assignment_Response
        fields = ['id', 'student_id', 'name', 'email','submited_date']

class NotSubmittedResponseListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_student_name')
    email = serializers.SerializerMethodField('get_student_email')


    def get_student_name(self, obj):
        return obj.student_id.name

    def get_student_email(self, obj):
        return obj.student_id.email

    class Meta:
        model = SubmissionStatus
        fields = ['name', 'email']

class GetTeacherAssignmentResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_student_name')
    email = serializers.SerializerMethodField('get_student_email')

    def get_student_name(self, obj):
        return obj.student_id.name

    def get_student_email(self, obj):
        return obj.student_id.email

    class Meta:
        model = Assignment_Response
        fields = ['name', 'email','student_id', 'submited_date', 'submission_file']

class GradeAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade_Assignment
        fields = '__all__'

class GetTeacherGradedResponseListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_student_name')
    email = serializers.SerializerMethodField('get_student_email')
    marks = serializers.SerializerMethodField('get_student_marks')

    def get_student_name(self, obj):
        return obj.student_id.name
    
    def get_student_email(self, obj):
        return obj.student_id.email

    def get_student_marks(self, obj):
        marks = Grade_Assignment.objects.get(response_id=obj.id).marks_scored
        return str(marks)


    class Meta:
        model = Assignment_Response
        fields = ['id', 'student_id', 'name', 'email','marks']

class GetTeacherGradedResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_student_name')
    email = serializers.SerializerMethodField('get_student_email')
    mark = serializers.SerializerMethodField('get_student_mark')
    remark = serializers.SerializerMethodField('get_student_remark')

    def get_student_name(self, obj):
        return obj.student_id.name

    def get_student_email(self, obj):
        return obj.student_id.email

    def get_student_mark(self, obj):
        marks = Grade_Assignment.objects.get(response_id=obj.id).marks_scored
        return str(marks)

    def get_student_remark(self, obj):
        remark = Grade_Assignment.objects.get(response_id=obj.id).remark
        return remark


    class Meta:
        model = Assignment_Response
        fields = ['student_id', 'name', 'email', 'submission_file', 'submited_date', 'mark', 'remark']
