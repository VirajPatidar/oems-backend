from django.db import models
from authentication.models import *

# Create your models here.

class Classes(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher')
    joining_code = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    joining_code_expiry_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name}_____{self.joining_code}_____{self.teacher_id} "
        
    #    return f"{self.name}    {self.joining_code}     {self.joining_code_expiry_date}    {self.teacher_id} "

    # create table class (
    # 	id integer PRIMARY KEY,
    # 	teacher_id integer REFERENCES teacher(id),
    # 	joining_code integer,
    # 	name text,
    # 	joining_code_expiry_date text
    # );


class Study(models.Model):
    
    class Meta:
        unique_together = (('class_id', 'student_id'),)

    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='classes')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')

    def __str__(self):
        return f"{self.class_id} #### {self.student_id}"


    # create table study (
    # 	class_id integer REFERENCES class(id),
    # 	student_id integer REFERENCES student(id),
    # 	PRIMARY KEY(class_id, student_id)
    # );