from django.urls import path
from .views import (
    MakeQuizView
)

urlpatterns = [
    path('make-quiz/', MakeQuizView.as_view(), name="make-quiz"),
]