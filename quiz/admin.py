from django.contrib import admin
from .models import Quiz, SubmissionStatus, Question, QuizResponse

# Register your models here.

admin.site.register(Quiz)
admin.site.register(SubmissionStatus)
admin.site.register(Question)
admin.site.register(QuizResponse)