from rest_framework import generics, permissions
from .models import Assignment, Submission
from .serializers import SubmissionSerializer, AssignmentSerializer

class AssignmentCreateView(generics.ListCreateAPIView):
    """An endpoint to create and list all the assignments associated with the course"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionCreateView(generics.CreateAPIView):
    """An endpoint for submission of assignment"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class SubmissionListView(generics.ListAPIView):
    """An endpoint to get all the submissions of tha assignment"""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(assignment__course__id = self.kwargs['course_id'])