from django.urls import path
from courses import views

urlpatterns = [
    path('instructor/<int:instructor_id>/', views.InstructorAPIView.as_view(), name='instructor'),
    path('instructor/register/', views.InstructorRegisterationAPIView.as_view(), name='instructor-register'),
    path('instructor/login/', views.InstructorLoginAPIView.as_view(), name='instructor-login'),
    path('instructor/logout/', views.InstructorLogoutAPIView.as_view(), name='instructor-logout'),
    path('instructor/courses/', views.InstructorCourseListCreateAPIView.as_view(), name='instructor-course'),
    path('instructor/courses/<int:pk>', views.InstructorCourseDetailAPIView.as_view(), name='instructor-course-detail'),
    path('instructor/enrollments/', views.InstructorCourseEnrollmentsAPIView.as_view(), name='instructor-course-enrollments'),

    path('courses/', views.CourseAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/enroll/', views.EnrollmentCreateAPIView.as_view(), name='course-enroll'),
    path('courses/<int:course_id>/lectures/', views.LectureListCreateAPIView.as_view(), name='lecture-list-create'),
    path('courses/<int:course_id>/lectures/<int:pk>/', views.LectureDetailAPIView.as_view(), name='lecture-detail'),

    path('courses/payment/', views.PaymentView.as_view(), name='payment')
    
]
