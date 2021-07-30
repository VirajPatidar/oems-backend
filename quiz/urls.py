from django.urls import path
from .views import (
    MakeQuizView,
    CreateQuestionView,
    GetTeachQuizView,
    GetStuQuizView,
    GetTeachQuestionView,
    GetStuQuestionView,
    SubmitQuizResponseView,
    ReleaseResponseView,
    QuizStatisticsView
)

urlpatterns = [
    path('make-quiz', MakeQuizView.as_view(), name="make-quiz"),
    path('make-question', CreateQuestionView.as_view(), name="make-question"),
    path('<int:class_id>', GetTeachQuizView.as_view(), name="teach-quiz"),
    path('<int:class_id>/<int:student_id>', GetStuQuizView.as_view(), name="stu-quiz"),
    path('question/<int:quiz_id>', GetTeachQuestionView.as_view(), name="teach-question"),
    path('question/<int:quiz_id>/<int:student_id>', GetStuQuestionView.as_view(), name="stu-question"),
    path('response/<int:quiz_id>/<int:student_id>', SubmitQuizResponseView.as_view(), name="quiz-response"),
    path('result/<int:quiz_id>', ReleaseResponseView.as_view(), name="quiz-result"),
    path('statistics/<int:class_id>/<int:quiz_id>', QuizStatisticsView.as_view(), name="quiz-statistics"),
]