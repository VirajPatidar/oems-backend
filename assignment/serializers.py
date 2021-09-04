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

class UpdateAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'instructions', 'total_marks', 'due_on', 'ques_file']

class SubmitAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Response
        fields = '__all__'

class UpdateAssignmentResponse(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Response
        fields = ['submission_file', 'submited_date']

class GetAssignmentResponseSerializer(serializers.ModelSerializer):

    submission_status = serializers.SerializerMethodField('get_submission_status')
    marks = serializers.SerializerMethodField('get_marks')
    remark = serializers.SerializerMethodField('get_remark')

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

    def get_remark(self, obj):
        if obj.isGraded==True:
            remark = Grade_Assignment.objects.get(response_id=obj.id).remark
            return remark
        else:
            return "Your Assignment is not yet Graded"

    def get_submission_status(self, obj):
        if obj.assignment_id.due_on > obj.submited_date:
            return 'Assignment Submitted Before Due'
        else:
            return 'Assignment Submitted Late'

    class Meta:
        model = Assignment_Response
        fields = ['id','submission_file', 'isGraded', 'submited_date', 'submission_status','marks', 'remark']


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
    submission_status = serializers.SerializerMethodField('get_submission_status')

    def get_student_name(self, obj):
        return obj.student_id.name

    def get_student_email(self, obj):
        return obj.student_id.email

    def get_submission_status(self, obj):
        if obj.assignment_id.due_on > obj.submited_date:
            return 'Assignment Submitted Before Due'
        else:
            return 'Assignment Submitted Late'

    class Meta:
        model = Assignment_Response
        fields = ['name', 'email','student_id', 'submited_date', 'submission_file', 'submission_status']

class GradeAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade_Assignment
        fields = '__all__'

class UpdateGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade_Assignment
        fields = ['marks_scored', 'remark']

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
    grade_id = serializers.SerializerMethodField('get_grade_id')

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
    
    def get_grade_id(self, obj):
        id=Grade_Assignment.objects.get(response_id=obj.id).id
        return id


    class Meta:
        model = Assignment_Response
        fields = ['student_id', 'name', 'email', 'submission_file', 'submited_date', 'grade_id', 'mark', 'remark']
