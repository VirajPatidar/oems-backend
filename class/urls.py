from django.urls import path
from .views import (
    HandleClassView,
    ClassMembershipView
)
urlpatterns = [
    path('manage-class/', HandleClassView.as_view(), name="manage-class"),
    path('member-class/', ClassMembershipView.as_view(), name="member-class"),
]