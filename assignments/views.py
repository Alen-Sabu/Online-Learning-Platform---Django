from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from courses.models import Enrollment
from .models import Assignment, Submission, Notification
from .serializers import SubmissionSerializer, AssignmentSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

CustomUser = get_user_model()

class AssignmentCreateView(generics.CreateAPIView):
    """An endpoint to create assignment by the instructor and send notifications"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        assignment = serializer.save()
        self.send_notification(assignment)

    def send_notification(self, assignment):
        enrolled_students = Enrollment.objects.filter(course = assignment.course).values_list('user', flat=True)
        students = CustomUser.objects.filter(id__in = enrolled_students)

        for student in students:
            notification = Notification.objects.create(
                user = student,
                assignment = assignment,
                message = f"New assignment posted {assignment.title}"
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{student.id}",
                {
                    "type": "send_notification",
                    "messsage": {
                        "id": notification.id,
                        "assignment": assignment.title,
                        "message": notification.message,
                        "created_at": str(notification.created_at),
                        "read": notification.read,
                    }
                }
            )

class AssignmentListView(generics.ListAPIView):
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