from django.db import models

from authentication.models import User
from klass.models import Classes

# Create your models here.

class SharedFolder(models.Model):
    title = models.CharField(max_length=100)
    filefield = models.FileField(blank=False, null=False, upload_to='shared_folder/')
    added_by = models.ForeignKey(User , on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}-{self.added_by}"
