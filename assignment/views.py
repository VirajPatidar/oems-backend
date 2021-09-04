from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import os
from django.conf import settings
from datetime import datetime

from oems_api.permissions import IsTeacher, IsStudent
from klass.models import Classes, Study
from .models import *
from .serializers import *

class CreateAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
    serializer_class = AssignmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        assign_data = serializer.data

        class_id = request.data.get('class_id')
        c = Classes.objects.get(pk = class_id)
        stu_ids = list(Study.objects.values_list('student_id', flat=True).filter(class_id=class_id))
        stu_objs = Student.objects.filter(id__in=stu_ids)
        assign = Assignment.objects.get(id=assign_data['id'])

        for i in stu_objs:
            SubmissionStatus.objects.create(class_id=c, student_id=i, assignment_id=assign)

        return Response(assign_data, status=status.HTTP_201_CREATED)


class GetTeachAssignmentListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
    serializer_class = AssignmentListSerializer

    def get(self, request, class_id):
        try:
            c = Classes.objects.get(id=class_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Class Id'
            }, status=status.HTTP_400_BAD_REQUEST)

        assignments = Assignment.objects.filter(class_id=class_id).order_by('due_on')
        if len(assignments)==0:
            return Response({
                'message':'No Assignments Available'
            }, status=status.HTTP_204_NO_CONTENT)
        
        serializer = AssignmentListSerializer(instance=assignments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTecherAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
    serializer_class = GetAssignmentSerializer

    def get(self, request, assign_id):
        try:
            assign = Assignment.objects.get(id=assign_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Assignment Id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GetAssignmentSerializer(instance=assign)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def patch(self, request, assign_id):
        try:
            assign = Assignment.objects.get(id=assign_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Assignment Id'
            }, status=status.HTTP_400_BAD_REQUEST)

        ques_file_url=os.path.join(settings.MEDIA_ROOT, assign.ques_file.name)
        print(ques_file_url)
        serializer = UpdateAssignmentSerializer(assign, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        if os.path.exists(ques_file_url) and request.data.get('ques_file'):
                print(True)
                os.remove(ques_file_url)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetStuAssignmentListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudent)
    serializer_class = AssignmentListSerializer

    def get(self, request, stu_id, class_id):
        assign_ids = SubmissionStatus.objects.values_list('assignment_id', flat=True).filter(class_id = class_id, student_id=stu_id)

        pending_assign_ids = list(assign_ids.filter(submission_status=False))
        pending_assignments = Assignment.objects.filter(id__in=pending_assign_ids).order_by('due_on')
        pending_assign_serializer = AssignmentListSerializer(instance=pending_assignments, many=True)

        submitted_assign_ids = list(assign_ids.filter(submission_status=True))
        submitted_assignments = Assignment.objects.filter(id__in=submitted_assign_ids).order_by('due_on')
        submitted_assign_serializer = AssignmentListSerializer(instance=submitted_assignments, many=True)

        return Response({
            'Pending': pending_assign_serializer.data,
            'Submitted': submitted_assign_serializer.data
        }, status=status.HTTP_200_OK)

class GetStudentPendingAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudent)
    serializer_class = GetAssignmentSerializer

    def get(self, request, assign_id):
        try:
            assign = Assignment.objects.get(id=assign_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Assignment Id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GetAssignmentSerializer(instance=assign)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitAssignmentResponseView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def post(self, request, assign_id, student_id):
        serializer = SubmitAssignmentSerializer(data={
            'assignment_id':assign_id,
            'student_id': student_id,
            'submission_file': request.data['submission_file']
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        submission_status = SubmissionStatus.objects.get(assignment_id=assign_id, student_id=student_id)
        submission_status.submission_status = True
        submission_status.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetStudentSubmitedAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def get(self, request, assign_id, student_id):
        try:
            assign = Assignment.objects.get(id=assign_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Assignment Id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GetAssignmentSerializer(instance=assign)

        assignment_response = Assignment_Response.objects.get(assignment_id=assign_id, student_id=student_id)
        response_serializer = GetAssignmentResponseSerializer(instance=assignment_response)

        return Response({
            "Assignment_Details":serializer.data,
            "Response_Details":response_serializer.data
            }, status=status.HTTP_200_OK)

class UpdateStudentSubmittedAssignmantView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def put(self, request, response_id):
        try:
            response_obj = Assignment_Response.objects.get(id=response_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Response Id'
            }, status=status.HTTP_400_BAD_REQUEST)

        if response_obj.isGraded==False:
            response_obj.submited_date = datetime.now(response_obj.submited_date.tzinfo)
            response_obj.save()
            submission_file_url=os.path.join(settings.MEDIA_ROOT, response_obj.submission_file.name)
            serializer = UpdateAssignmentResponse(response_obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            if os.path.exists(submission_file_url):
                print(True)
                os.remove(submission_file_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'You submission is graded so you can not update submission file'
            }, status=status.HTTP_304_NOT_MODIFIED)

        



class GetTeacherAssignmentResponseList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, assign_id):
        submitted_response_objs = Assignment_Response.objects.filter(assignment_id=assign_id, isGraded=False)

        submitted_serializer = GetTeacherAssignmentResponseListSerializer(instance=submitted_response_objs, many=True)

        not_submitted_response = SubmissionStatus.objects.filter(assignment_id=assign_id, submission_status=False)

        not_submitted_serializer = NotSubmittedResponseListSerializer(instance=not_submitted_response, many=True)

        return Response({
            'Submitted_Responses':submitted_serializer.data,
            'Not_Submitted_Responses':not_submitted_serializer.data
        }, status=status.HTTP_200_OK)

class GetTeacherAssignmentResponse(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, response_id):
        submitted_response_obj = Assignment_Response.objects.get(id=response_id)
        serializer = GetTeacherAssignmentResponseSerializer(instance=submitted_response_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)        


class GradeAssignmentView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
    serializer_class = GradeAssignmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        grade_data = serializer.data

        response_id = request.data.get('response_id')

        response_obj = Assignment_Response.objects.get(id=response_id)
        print(response_obj)
        response_obj.isGraded = True
        response_obj.save()

        stu_id = response_obj.student_id
        assign_id = response_obj.assignment_id

        sub_status_obj = SubmissionStatus.objects.get(student_id=stu_id, assignment_id=assign_id)
        print(sub_status_obj)
        sub_status_obj.marks_scored = request.data.get('marks_scored')
        sub_status_obj.save()

        return Response(grade_data, status=status.HTTP_201_CREATED)

class UpdateAssignmentGradeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def put(self, request, grade_id):
        try:
            grade_obj = Grade_Assignment.objects.get(id=grade_id)
        except ObjectDoesNotExist:
            return Response({
                'message':'Invalid Grade Id'
            }, status=status.HTTP_400_BAD_REQUEST) 

        serializer = UpdateGradeSerializer(grade_obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        grade_data = serializer.data
        
        stu_id = grade_obj.response_id.student_id
        assign_id = grade_obj.response_id.assignment_id

        sub_status_obj = SubmissionStatus.objects.get(student_id=stu_id, assignment_id=assign_id)
        sub_status_obj.marks_scored = request.data.get('marks_scored')
        sub_status_obj.save()

        return Response(grade_data, status=status.HTTP_200_OK)



class GetTeacherGradedResponseList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, assign_id):
        graded_response_objs = Assignment_Response.objects.filter(assignment_id=assign_id, isGraded=True)

        serializer = GetTeacherGradedResponseListSerializer(instance=graded_response_objs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class GetTeacherGradedResponse(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, response_id):
        response_obj = Assignment_Response.objects.get(id=response_id)

        serializer = GetTeacherGradedResponseSerializer(instance=response_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)
