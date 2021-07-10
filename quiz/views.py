from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .permissions import IsTeacher, IsStudent
from .models import *
from klass.models import Classes, Study
from authentication.models import *
from .serializers import (
    QuizSerializer
)
from django.core.exceptions import ObjectDoesNotExist

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