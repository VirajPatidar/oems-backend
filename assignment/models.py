from django.db import models
from datetime import datetime




from klass.models import Classes
from authentication.models import Student


# Create your models here.
class Assignment(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    total_marks = models.IntegerField()
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='assignment_class_id')
    marks_released = models.BooleanField(default=False)
    due_on = models.DateTimeField()
    ques_file = models.FileField(blank=True, null=True, upload_to='questions_file_folder/')


    def assignment_status(self):
        if datetime.now(self.due_on.tzinfo) < self.due_on:
            return "Due on:" + str(self.due_on)
        else:
            return "Overdue"
    
    def __str__(self):
        return f"{self.class_id}-{self.name}"


class SubmissionStatus(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='assign_status_class_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assign_status_student_id')
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_submission_status')
    submission_status = models.BooleanField(default=False)
    marks_scored = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_id}-{self.student_id}-{self.assignment_id}-{self.submission_status}"

class Assignment_Response(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='response_assignment_id')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assign_response_student_id')
    submission_file = models.FileField(blank=False, null=False, upload_to='submissions/')
    submited_date = models.DateTimeField(auto_now_add=True)
    isGraded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.assignment_id}-{self.student_id}"

class Grade_Assignment(models.Model):
    response_id = models.ForeignKey(Assignment_Response, on_delete=models.CASCADE, related_name='grade_assignment_response_id')
    marks_scored = models.IntegerField()
    remark = models.TextField(blank=True)

    def __str__(self):
        return f"{self.response_id}-{self.marks_scored}"