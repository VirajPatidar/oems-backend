from django.contrib import admin
from .models import Quiz, Status, Question, Response

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Status)
admin.site.register(Question)
admin.site.register(Response)