from django.urls import path
from .views import AssignmentListView, SubmissionCreateView, SubmissionListView, AssignmentCreateView

urlpatterns = [
    path('',AssignmentListView.as_view(), name='assignment-create'),
    path('create-assignment/', AssignmentCreateView.as_view(), name='create-assignment'),
    path('<int:course_id>/submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submit/', SubmissionCreateView.as_view(), name='submit-create'),
]
