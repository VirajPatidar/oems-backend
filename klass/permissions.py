from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_object_permission(self, request):
        return request.user.user_type=="student"

class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request):
        return request.user.user_type=="teacher"

# permission_classes = (permissions.IsAuthenticated,IsOwner)