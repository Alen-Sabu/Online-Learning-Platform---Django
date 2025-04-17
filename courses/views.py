import stripe.error
import stripe
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateAPIView, 
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    get_object_or_404, )
from rest_framework.permissions import AllowAny, IsAuthenticated
from courses import serializers
from courses.models import Course,Category, Enrollment, Lecture, LectureProgress, Payment
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from instructor.permissions import IsInstructorAndOwner

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()
     
class CourseAPIView(ListAPIView):
    """
    Get all the courses
    """
    queryset = Course.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.CourseSerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [AllowAny]

class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseDetailSerializer
    permission_classes = (AllowAny,)

class LectureDetailAPIView(RetrieveUpdateAPIView):
    """
    An endpoint to update and delete each lectures of a course
    """
    serializer_class = serializers.LectureSerializer
    queryset = Lecture.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method in ["PUT","PATCH", "DELETE"]:
            self.permission_classes = (IsInstructorAndOwner,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

class MarkLectureCompleteView(UpdateAPIView):
    serializer_class = serializers.LectureProgressSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        lecture_id = kwargs.get("lecture_id")
        progress, created = LectureProgress.objects.get_or_create(
             user = request.user,
             lesson_id=lecture_id
        )

        progress.completed = True
        progress.save()
        return Response({"message": "Lecture marked as completed", "completed": progress.completed})
      
class MyCoursesView(ListAPIView):
    """Retrieve courses the authenticated user is enrolled in"""
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = Enrollment.objects.filter(user=self.request.user)
        return data
  
class EnrollmentCreateAPIView(CreateAPIView):
    """
    An endpoint to enroll users to each course
    """
    serializer_class = serializers.EnrollmentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
    
        serializer.is_valid(raise_exception = True)
        enrollment = serializer.save()
    
        return Response({"message": "Successfully enrolled in the course"}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)

            user = request.user

        # Check if user is already enrolled
            if Enrollment.objects.filter(user=user, course=course).exists():
                return Response(
                {"detail": "You are already enrolled in this course."},
                status=status.HTTP_400_BAD_REQUEST
            )

            if course.price <= 0:
                return Response({"error": "Course is free. No payment needed."}, status=400)

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=user.email, 
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": course.title,
                        },
                        "unit_amount": int(course.price * 100),
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url='http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:5173/cancel',
                metadata={
                    "course_id": str(course.id),
                    "user_id": str(request.user.id),
                },
            )
          
            return Response({"session_id": session.id})
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session.get('customer_email')
            course_id = session.get('metadata', {}).get('course_id')

            try:
                course = Course.objects.get(id=course_id)
                user = User.objects.get(email=customer_email)

                # Prevent duplicate enrollments
                if not Enrollment.objects.filter(user=user, course=course).exists():
                    Enrollment.objects.create(user=user, course=course)
            except Exception as e:
                print("Enrollment error:", e)

        return Response(status=status.HTTP_200_OK)
    

    
class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.GET.get("session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                return Response({"message": "Payment verified and enrollment completed."})
            return Response({"error": "Payment not completed"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
