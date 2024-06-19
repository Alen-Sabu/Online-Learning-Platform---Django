from rest_framework.permissions import BasePermission

class IsInstructorAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_instructor and obj.instructor.user == request.user