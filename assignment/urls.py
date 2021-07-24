from django.urls import path
from .views import *

urlpatterns = [
    path('create-assignment', CreateAssignmentView.as_view(), name='create-assignmant'),
    path('<int:class_id>/list', GetTeachAssignmentListView.as_view(), name='teacher-assignment-list'),
    path('<int:assign_id>/teacher', GetTecherAssignmentView.as_view(), name='teacher-assignment'),
    path('<int:stu_id>/<int:class_id>/list', GetStuAssignmentListView.as_view(), name='student-assignment-list'),
    path('<int:assign_id>/student', GetStudentAssignmentView.as_view(), name='student-assignment'),
    
]