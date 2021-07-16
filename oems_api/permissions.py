from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type=="student"

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type=="teacher"