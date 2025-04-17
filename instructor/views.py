from django.shortcuts import render
from rest_framework.generics import (
    GenericAPIView, 
    RetrieveUpdateAPIView, 
    ListAPIView, 
    RetrieveAPIView,
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    CreateAPIView,
    UpdateAPIView,
    get_object_or_404, )
# Create your views here.
from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, EnrollmentSerializer
from instructor import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from instructor.models import Instructor
from instructor.permissions import IsInstructorAndOwner
from .mixins import tagged_view
from django.contrib.auth import authenticate
from rest_framework.views import APIView

@tagged_view('Instructor')
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
    
@tagged_view('Instructor')
class InstructorLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing instructors
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.InstructorLoginSerializer

    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None and hasattr(user, 'instructor'):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': 'instructor',
                },
                
            })
        return Response({'detail': 'Invalid credentials or not an instructor'}, status=status.HTTP_401_UNAUTHORIZED)
    
@tagged_view('Instructor')
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
        
@tagged_view('Instructor')
class InstructorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
            instructor = request.user.instructor
        except Instructor.DoesNotExist:
            return Response({'detail': 'User is not an instructor'}, status=403)

        courses = Course.objects.filter(instructor=instructor)
        serializer = CourseSerializer(courses, many=True)
        return Response({'courses': serializer.data})       

@tagged_view('Instructor')
class InstructorAPIView(RetrieveUpdateAPIView):
    """
    Get, update Instructor information
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InstructorSerializer

    def get_object(self):
        return self.request.user.instructor
    

@tagged_view('Instructor')
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


@tagged_view('Instructor')
class InstructorCourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update, and destroy a course for authenticated instructors
    """
    queryset = Course.objects.all()
    serializer_class = serializers.InstructorCourseSerializer
    permission_classes = (IsInstructorAndOwner,)

@tagged_view('Instructor')
class InstructorCourseEnrollmentsAPIView(ListAPIView):
    """
    An endpoint to get all the users enrolled for each course
    """
    serializer_class = EnrollmentSerializer
    permission_classes = (IsInstructorAndOwner,)
    def get_queryset(self):
        instructor = self.request.user.instructor
        return Enrollment.objects.filter(course__instructor = instructor)
   