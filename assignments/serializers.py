from rest_framework import serializers
from .models import Assignment, Submission

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