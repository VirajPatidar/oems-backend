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

    def quiz_status(self):
        if (datetime.now(self.start_time.tzinfo) < self.start_time):
            return "Due on: "+str(self.start_time)
        elif (self.start_time < datetime.now(self.start_time.tzinfo)) and (datetime.now(self.end_time.tzinfo) < self.end_time):
            return "Active"
        elif (self.end_time < datetime.now(self.end_time.tzinfo)):
            return "Overdue"    

    def __str__(self):
        return f"{self.class_id}_____{self.name}"


class SubmissionStatus(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='status_class_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='status_student_id')
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_submission_status')
    submission_status = models.BooleanField(default=False)
    marks_scored = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_id}_____{self.student_id}_____{self.quiz_id}_____{self.submission_status}"


class Question(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=250, blank=True)
    marks = models.IntegerField()
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    correct_option_number = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_id}_____{self.question}"


class QuizResponse(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='response_quiz_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='response_student_id')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_id')
    question = models.CharField(max_length=250, blank=True)
    marks = models.IntegerField()
    marks_scored = models.IntegerField(default=0)
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    correct_option_number = models.IntegerField()
    marked_option_number = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_id}_____{self.student_id}_____{self.question}"