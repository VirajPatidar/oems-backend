from django.urls import path
from .views import *

urlpatterns = [
    path('create-assignment', CreateAssignmentView.as_view(), name='create-assignmant'),
    path('<int:class_id>/list', GetTeachAssignmentListView.as_view(), name='teacher-assignment-list'),
    path('<int:assign_id>/teacher', GetTecherAssignmentView.as_view(), name='teacher-assignment'),
    path('<int:assign_id>/update-assignment', UpdateAssignmentView.as_view(), name='update-assignment'),
    path('<int:stu_id>/<int:class_id>/list', GetStuAssignmentListView.as_view(), name='student-assignment-list'),
    path('<int:assign_id>/student/pending', GetStudentPendingAssignmentView.as_view(), name='student-pending-assignment'),
    path('<int:assign_id>/<int:student_id>/submit', SubmitAssignmentResponseView.as_view(), name='submit-assignment-response'),
    path('<int:assign_id>/<int:student_id>/submitted', GetStudentSubmitedAssignmentView.as_view(), name='submitted-assignment'),
    path('<int:response_id>/update-response', UpdateStudentSubmittedAssignmantView.as_view(), name='update-assignment-response'),
    path('<int:assign_id>/response-list', GetTeacherAssignmentResponseList.as_view(), name='teacher-assignment-response-list'),
    path('<int:response_id>/response', GetTeacherAssignmentResponse.as_view(), name='teacher-assignment-response'),
    path('grade-assignment', GradeAssignmentView.as_view(), name='grade-assignment'),
    path('<int:assign_id>/graded-response-list', GetTeacherGradedResponseList.as_view(), name='teacher-graded-response-list'),
    path('<int:response_id>/graded-response', GetTeacherGradedResponse.as_view(), name='teacher-graded-response'),
    path('<int:grade_id>/update-grade', UpdateAssignmentGradeView.as_view(), name='update-assignment-grade'),    
]