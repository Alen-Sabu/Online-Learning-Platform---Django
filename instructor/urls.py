from django.urls import path,include
from . import views


urlpatterns = [
    path('<int:instructor_id>/', views.InstructorAPIView.as_view(), name='instructor'),
    path('register/', views.InstructorRegisterationAPIView.as_view(), name='instructor-register'),
    path('login/', views.InstructorLoginAPIView.as_view(), name='instructor-login'),
    path('logout/', views.InstructorLogoutAPIView.as_view(), name='instructor-logout'),
    path('dashboard/', views.InstructorDashboardView.as_view(), name='instructor-dashboard'),
    path('courses/', views.InstructorCourseListCreateAPIView.as_view(), name='instructor-course'),
    path('courses/<int:pk>', views.InstructorCourseDetailAPIView.as_view(), name='instructor-course-detail'),
    path('enrollments/', views.InstructorCourseEnrollmentsAPIView.as_view(), name='instructor-course-enrollments'),
]