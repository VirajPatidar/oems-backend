from django.db import models
from klass.models import Classes
from authentication.models import Student
from datetime import datetime

# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=50, blank=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='quiz_class_id')
    number_of_questions = models.IntegerField()
    marks = models.IntegerField()
    response_released = models.BooleanField(default=False)
    start_time = models.DateTimeField()    
    end_time = models.DateTimeField()

    def isActive(self):
        if (self.start_time < datetime.now()) and (datetime.now() < self.end_time):
            return True
        else:
            return False    

    def __str__(self):
        return f"{self.class_id}_____{self.name}"


class Status(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='status_class_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='status_student_id')
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='status_quiz_id')
    submission_status = models.BooleanField(default=False)
    marks_scored = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_id}_____{self.student_id}_____{self.quiz_id}_____{self.submission_status}"


class Question(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_quiz_id')
    question = models.CharField(max_length=250, blank=True)
    marks = models.IntegerField()
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    correct_option_number = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_id}_____{self.question}"


class Response(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='response_quiz_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='response_student_id')
    question = models.CharField(max_length=250, blank=True)
    marks = models.IntegerField()
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    correct_option_number = models.IntegerField()
    marked_option_number = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_id}_____{self.student_id}_____{self.question}"