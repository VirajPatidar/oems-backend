from django.urls import path
from .views import (
    HandleClassView,
    ClassMembershipView,
    AddRemoveStudentView,
    ClassMembersListView,
    ClassListView
)
urlpatterns = [
    path('manage-class', HandleClassView.as_view(), name="manage-class"),
    path('member-class', ClassMembershipView.as_view(), name="member-class"),
    path('manage-student', AddRemoveStudentView.as_view(), name="manage-student"),
    path('class-list/<int:class_id>', ClassMembersListView.as_view(), name="class-member-list"),
    path('<int:id>', ClassListView.as_view(), name="class-list"),
]