from django.urls import path
from .views import (
    MakeQuizView,
    CreateQuestionView,
    GetTeachQuizView,
    GetStuQuizView,
    GetTeachQuestionView,
    GetStuQuestionView,
    SubmitQuizResponseView
)

urlpatterns = [
    path('make-quiz/', MakeQuizView.as_view(), name="make-quiz"),
    path('make-question/', CreateQuestionView.as_view(), name="make-question"),
    path('quiz/<class_id>', GetTeachQuizView.as_view(), name="teach-quiz"),
    path('quiz/<class_id>/<student_id>', GetStuQuizView.as_view(), name="stu-quiz"),
    path('question/<quiz_id>', GetTeachQuestionView.as_view(), name="teach-question"),
    path('question/<quiz_id>/<student_id>', GetStuQuestionView.as_view(), name="stu-question"),
    path('response/<quiz_id>/<student_id>', SubmitQuizResponseView.as_view(), name="quiz-response"),
]