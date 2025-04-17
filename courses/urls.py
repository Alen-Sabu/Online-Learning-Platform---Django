from django.urls import path,include
from courses import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
  
    path('courses/', views.CourseAPIView.as_view(), name='courses'),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path('courses/<int:pk>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('lectures/<int:pk>/', views.LectureDetailAPIView.as_view(), name='lecture-detail'),
    path('lectures/<int:lecture_id>/complete/', views.MarkLectureCompleteView.as_view(), name="mark-lecture-complete"),
    path("my-courses/", views.MyCoursesView.as_view(), name='my-courses'),

    path('courses/enroll/', views.EnrollmentCreateAPIView.as_view(), name='course-enroll'),

    path('courses/payment/', views.PaymentView.as_view(), name='payment'),
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('courses/verify-payment/', views.VerifyPaymentView.as_view()),
    
]
