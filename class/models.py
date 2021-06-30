from django.db import models
from authentication.models import *

# Create your models here.

class Classes(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher')
    joining_code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    joining_code_expiry_date = models.DateField()

    def __str__(self):
        return f"{self.name}_____{self.joining_code}_____{self.teacher_id}_____{self.joining_code_expiry_date}"


class Study(models.Model):
    
    class Meta:
        unique_together = (('class_id', 'student_id'),)

    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='classes')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')

    def __str__(self):
        return f"{self.class_id} #### {self.student_id}"