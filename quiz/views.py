from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from oems_api.permissions import IsTeacher, IsStudent
from .models import *
from klass.models import Classes, Study
from authentication.models import *
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    GetQuizSerializer,
    QuizQuestionSerializer,
    TeachQuizQuestionSerializer,
    QuizResponseSerializer,
    QuizStatisticsSerializer
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


class GetTeachQuestionView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, quiz_id):

        try:
            quiz = Quiz.objects.get(pk = quiz_id)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid quiz ID'})
            
        quiz = TeachQuizQuestionSerializer(instance=quiz)
        return Response(quiz.data)

class GetStuQuestionView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def get(self, request, quiz_id, student_id):

        try:
            quiz = Quiz.objects.get(pk = quiz_id)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid quiz ID'})

        quiz_status = quiz.quiz_status()
        print(quiz_status)

        response_released = quiz.response_released
        print(response_released)

        try:
            submission_status = SubmissionStatus.objects.values('submission_status').filter(quiz_id = quiz_id, student_id=student_id)[0]['submission_status']
        except IndexError:
            return Response({'response':'Invalid student ID'})
        
        print(submission_status)

        if submission_status :
            if response_released :
                submit_status = SubmissionStatus.objects.get(quiz_id=quiz_id, student_id=student_id)
                quiz_response = QuizResponse.objects.filter(quiz_id=quiz_id, student_id=student_id)
                resp = QuizResponseSerializer(instance=quiz_response, many=True)
                return Response({'name':quiz.name, 'number_of_questions':quiz.number_of_questions, 'marks_scored': submit_status.marks_scored, 'total_marks':quiz.marks, 'quiz_response': resp.data})

            else :
                return Response({'name':quiz.name, 'response':'Result has not been released yet. Please contact your teacher'})

        else :
            if quiz_status == "Active" :
                quiz = QuizQuestionSerializer(instance=quiz)
                return Response(quiz.data)

            elif quiz_status == "Overdue" :
                return Response({'name':quiz.name, 'response':'This quiz is no longer accepting responses. Please contact your teacher'})

            else :
                return Response({'name':quiz.name, 'start_time': quiz.start_time, 'response':'Quiz will start on ' + str(quiz.start_time)[0:10] +' '+ str(quiz.start_time)[11:16]})


class SubmitQuizResponseView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def post(self, request, quiz_id, student_id):

        for i in request.data:
            question = Question.objects.get(pk = int(i.get('question_id')))
            serializer = QuizResponseSerializer(data={'quiz_id': quiz_id, 
                                                'student_id': student_id, 
                                                'question_id': int(i.get('question_id')), 
                                                'question': question.question,
                                                'marks': question.marks,
                                                'marks_scored': question.marks if question.correct_option_number == int(i.get('marked_option_number')) else 0,
                                                'option1': question.option1,
                                                'option2': question.option2,
                                                'option3': question.option3,
                                                'option4': question.option4,
                                                'correct_option_number': question.correct_option_number,
                                                'marked_option_number': int(i.get('marked_option_number'))
                                                })

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            print(i)


        quiz_response = QuizResponse.objects.filter(quiz_id=quiz_id, student_id=student_id)

        total_marks = 0
        for i in quiz_response:
            total_marks = total_marks + i.marks_scored

        submission_status = SubmissionStatus.objects.get(quiz_id=quiz_id, student_id=student_id)
        submission_status.marks_scored = total_marks
        submission_status.submission_status = True
        submission_status.save()

        resp = QuizResponseSerializer(instance=quiz_response, many=True)

        return Response(resp.data)


class ReleaseResponseView(generics.GenericAPIView):
    serializer_class = QuestionSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def post(self, request, quiz_id):

        try:
            quiz = Quiz.objects.get(pk = quiz_id)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid quiz ID'})

        quiz.response_released = True
        quiz.save()

        return Response({'response':'Result and response of '+quiz.name+ ' has been released'})



class QuizStatisticsView(generics.GenericAPIView):
    serializer_class = QuizStatisticsSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get(self, request, class_id, quiz_id):

        try:
            quiz = Quiz.objects.get(pk = quiz_id)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid quiz ID'})

        try:
            klass = Classes.objects.get(pk = class_id)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid quiz ID'})

        resp = QuizStatisticsSerializer(instance=quiz)

        return Response(resp.data)