from django.urls import path
from .views import (
    HandleMessageView
)
urlpatterns = [
    path('message/<class_id>', HandleMessageView.as_view(), name="getchatmessages"),
    path('message/', HandleMessageView.as_view(), name="chatmessage"),
]