from django.urls import path
from .views import (
    HandleMessageView,
    GetMessageView
)
urlpatterns = [
    path('message', HandleMessageView.as_view(), name="chatmessage"),
    path('message/<class_id>', GetMessageView.as_view(), name="getchatmessages"),
]