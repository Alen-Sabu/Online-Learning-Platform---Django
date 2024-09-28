from rest_framework import serializers
from .models import Assignment, Submission, Notification

class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer class for assignment"""
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date']

class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer class for Submission of the assignment"""
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'user', 'file', 'submitted_at']

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer class for notifications"""
    class Meta:
        model = Notification
        fields = ['id', 'user', 'assignment', 'message', 'created_at', 'read']