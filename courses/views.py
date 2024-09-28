import stripe.error
import stripe
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView, 
    RetrieveUpdateAPIView, 
    ListAPIView, 
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    CreateAPIView,
    get_object_or_404, )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import Serializer
from courses import serializers
from courses.models import Course, Enrollment, Lecture, Payment
from courses.permissions import IsInstructorAndOwner
from drf_yasg.utils import swagger_auto_schema

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


class InstructorRegisterationAPIView(GenericAPIView):
    """
    An endpoint for registeration of instructor
    """
    serializer_class = serializers.InstructorRegisterationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data 
        data['tokens'] = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)
    
class InstructorLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing instructors
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.InstructorLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        serializer = serializers.InstructorSerializer(user.instructor)
        token = RefreshToken.for_user(user)
        data = serializer.data 
        data['tokens'] = {'refresh': str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    
class InstructorLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout existing instructor
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = Serializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status = status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class InstructorAPIView(RetrieveUpdateAPIView):
    """
    Get, update Instructor information
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InstructorSerializer

    def get_object(self):
        return self.request.user.instructor

class InstructorCourseListCreateAPIView(ListCreateAPIView):
    """
    An endpoint to retrieve and create courses for authenticated instructors
    """
    serializer_class = serializers.InstructorCourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Course.objects.filter(instructor__user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(instructor = self.request.user.instructor)

class InstructorCourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update, and destroy a course for authenticated instructors
    """
    queryset = Course.objects.all()
    serializer_class = serializers.InstructorCourseSerializer
    permission_classes = (IsInstructorAndOwner,)

class CourseAPIView(ListAPIView):
    """
    Get all the courses
    """
    queryset = Course.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.CourseSerializer

class InstructorCourseEnrollmentsAPIView(ListAPIView):
    """
    An endpoint to get all the users enrolled for each course
    """
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = (IsInstructorAndOwner,)

    def get_queryset(self):
        instructor = self.request.user.instructor
        return Enrollment.objects.filter(course__instructor = instructor)
        
class EnrollmentCreateAPIView(CreateAPIView):
    """
    An endpoint to enroll users to each course
    """
    serializer_class = serializers.EnrollmentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        enrollment = self.perform_create(serializer)
        course_serializer = serializers.CourseSerializer(enrollment.course)
        data = course_serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
class LectureListCreateAPIView(ListCreateAPIView):
    """
    An endpoint to get the lectures of a course and create the lecture for each course
    """
    serializer_class = serializers.LectureSerializer

    def get_queryset(self):
        return Lecture.objects.filter(course_id = self.kwargs['course_id'])
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsInstructorAndOwner,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, id = self.kwargs['course_id'])
        serializer.save(course = course)

class LectureDetailAPIView(RetrieveUpdateAPIView):
    """
    An endpoint to update and delete each lectures of a course
    """
    serializer_class = serializers.LectureSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Lecture.objects.filter(course_id = self.kwargs['course_id'])
    
    def get_permissions(self):
        if self.request.method in ["PUT","PATCH", "DELETE"]:
            self.permission_classes = (IsInstructorAndOwner,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()
    
class PaymentView(APIView):
    def post(self, request):
        serializer = serializers.PaymentSerializer(data = request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            currency = serializer.validated_data['currency']
            source = serializer.validated_data['source']

            try:
                charge = stripe.Charge.create(
                    amount=int(amount * 100),
                    currency=currency,
                    source=source,
                    description='Payment Charge'
                )

                #save payment details to database (optional)
                Payment.objects.create(
                    stripe_charge_id = charge.id,
                    amount = amount,
                    success = True
                )
                return Response({'message': 'Payment successful', 'charge_id': charge.id}, status=status.HTTP_200_OK)
            except stripe.error.StripeError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
