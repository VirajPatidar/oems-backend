from django.db import models
from klass.models import Classes

# Create your models here.

class Chat(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='chat_class_id')
    message = models.CharField(max_length=200, blank=False)
    sent_by = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"{self.class_id}_____{self.message}_____{self.sent_by}"