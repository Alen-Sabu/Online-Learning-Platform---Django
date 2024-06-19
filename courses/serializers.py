from rest_framework import serializers
from courses.models import Instructor, Course, Lecture, Enrollment
from django.contrib.auth import get_user_model, authenticate
from users.serializers import CustomUserSerializer

User = get_user_model()

class InstructorSerializer(serializers.ModelSerializer):
    """
    Serialzier class for instructor
    """
    user = CustomUserSerializer()
    class Meta:
        model = Instructor
        fields = ['id', 'user', 'bio', 'profile_picture']

class InstructorRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class for instructor registeration
    """
    email = serializers.EmailField(required = True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            is_instructor = True
        )
        Instructor.objects.create(user = user)
        return user
    
class InstructorLoginSerializer(serializers.Serializer):
    """
    Serializer class for instructor login
    """
    email = serializers.CharField(required = True)
    password = serializers.CharField(write_only = True, required = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email = email, password = password)
            if user and user.is_active and user.is_instructor:
                return {'user':user, 'email': user.email}
            else:
                return serializers.ValidationError("Invalid credentials")
        else:
            return serializers.ValidationError("Both the fields are required")
        
class InstructorCourseSerializer(serializers.ModelSerializer):
    """
    Serializer class for specific course of the instructor
    """
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'created_at', 'updated_at']
        read_only_fields = ['instructor', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer class for courses
    """
    instructor = InstructorSerializer(read_only = True)
    class Meta:
        model = Course
        fields = ['id', 'instructor', 'title', 'description', 'created_at', 'thumbnail']

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer class to get the users enrolled for each course for instructors
    """
    user = CustomUserSerializer(read_only = True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'enrolled_at']

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer class to enroll the users for each course
    """
    class Meta:
        model = Enrollment
        fields = ['course']

    def create(self, validated_data):
        user = self.context['request'].user
        course = validated_data['course']
        enrollment, created = Enrollment.objects.get_or_create(user = user, course = course)
        if not created:
            raise serializers.ValidationError("You are already enrolled in this course")
        return enrollment
    
class LectureSerializer(serializers.ModelSerializer):
    """
    Serializer class for each lecture in a course
    """
    class Meta:
        model = Lecture
        fields = ['id', 'course', 'title', 'description', 'video_file', 'video_thumbnail', 'created_at']
        read_only_fields = ['id', 'created_at']