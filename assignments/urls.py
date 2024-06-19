from django.urls import path
from .views import AssignmentCreateView, SubmissionCreateView, SubmissionListView

urlpatterns = [
    path('',AssignmentCreateView.as_view(), name='assignment-create'),
    path('<int:course_id>/submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submit/', SubmissionCreateView.as_view(), name='submit-create'),
]
