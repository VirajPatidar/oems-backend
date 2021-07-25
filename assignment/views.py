from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

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

# class GetTeacherAssignmentResponseList(generics.GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated, IsTeacher)

#     def get(self, request, assign_id):
#         response_objs = SubmissionStatus.objects.filter(assignment_id=assign_id)
