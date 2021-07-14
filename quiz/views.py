from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .permissions import IsTeacher, IsStudent
from .models import *
from klass.models import Classes, Study
from authentication.models import *
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    GetQuizSerializer,
    QuizQuestionSerializer
)
from django.core.exceptions import ObjectDoesNotExist
import logging

# Create your views here.

class MakeQuizView(generics.GenericAPIView):
    serializer_class = QuizSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        quiz_data = serializer.data

        class_id = request.data.get('class_id')
        c = Classes.objects.get(pk = class_id)
        stu_ids = Study.objects.values_list('student_id', flat=True).filter(class_id = class_id)
        stu_ids = list(stu_ids)
        stu = Student.objects.filter(id__in = stu_ids)
        q = Quiz.objects.get(pk = quiz_data['id'])
        
        for i in stu:
            SubmissionStatus.objects.create(class_id=c, student_id=i, quiz_id=q)

        return Response(quiz_data, status=status.HTTP_201_CREATED)


class CreateQuestionView(generics.GenericAPIView):
    serializer_class = QuestionSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        question_data = serializer.data

        return Response(question_data, status=status.HTTP_201_CREATED)


class GetTeachQuizView(generics.GenericAPIView):
    serializer_class = GetQuizSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, class_id):

        quizzes = Quiz.objects.filter(class_id = class_id).order_by('start_time')
        print(len(quizzes))
        if len(quizzes) == 0 :
            return Response({'response':'Invalid class ID'})

        serializer = GetQuizSerializer(instance=quizzes, many=True)
        return Response(serializer.data)

class GetStuQuizView(generics.GenericAPIView):
    serializer_class = GetQuizSerializer

    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def get(self, request, class_id, student_id):

        quiz_ids = SubmissionStatus.objects.values_list('quiz_id', flat=True).filter(class_id = class_id, student_id=student_id)

        pending_quiz_ids = list(quiz_ids.filter(submission_status = False))
        pending_quizzes = Quiz.objects.filter(id__in = pending_quiz_ids).order_by('start_time')
        pending_serializer = GetQuizSerializer(instance=pending_quizzes, many=True)
        
        submitted_quiz_ids = list(quiz_ids.filter(submission_status = True))
        submitted_quizzes = Quiz.objects.filter(id__in = submitted_quiz_ids).order_by('start_time')
        submitted_serializer = GetQuizSerializer(instance=submitted_quizzes, many=True)

        return Response({'pending' : pending_serializer.data, 'submitted': submitted_serializer.data})


class GetStuQuestionView(generics.GenericAPIView):
    serializer_class = GetQuizSerializer

    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def get(self, request, quiz_id, student_id):

        quiz = Quiz.objects.get(pk = quiz_id)

        quiz_status = quiz.quiz_status()
        print(quiz_status)

        response_released = quiz.response_released
        print(response_released)

        submission_status = SubmissionStatus.objects.values('submission_status').filter(quiz_id = quiz_id, student_id=student_id)[0]['submission_status']
        print(submission_status)

        if submission_status :
            if response_released :
                pass

            else :
                return Response({'response':'Result has not been released yet. Please contact your teacher'})

        else :
            if quiz_status == "Active" :
                quiz = QuizQuestionSerializer(instance=quiz)
                return Response(quiz.data)

            elif quiz_status == "Overdue" :
                return Response({'response':'This quiz is no longer accepting responses. Please contact your teacher'})

            else :
                return Response({'response':'Quiz will start on ' + str(quiz.start_time)[0:10] +' '+ str(quiz.start_time)[11:16]})