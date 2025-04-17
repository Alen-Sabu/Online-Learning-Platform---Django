from rest_framework import serializers
from courses.models import Instructor, Category, Course, Lecture, Enrollment, LectureProgress
from django.contrib.auth import get_user_model, authenticate
from users.serializers import CustomUserSerializer
from instructor.serializers import InstructorSerializer

User = get_user_model()
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer class for courses
    """
    instructor = InstructorSerializer(read_only = True)
    category = CategorySerializer(read_only = True)

    class Meta:
        model = Course
        fields = ['id', 'instructor','category', 'title', 'description', 'created_at','price','thumbnail']

class LectureProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureProgress
        fields = ['id','lesson', 'completed','progress']

    
class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer class to get the users enrolled for each course for instructors
    """
    user = CustomUserSerializer(read_only = True)
    course = CourseSerializer(read_only=True) 
    lesson_progress = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'enrolled_at','course','progress', 'lesson_progress']
    
    def get_progress(self, obj):
        total_lessons = obj.course.lecture.count()
        if total_lessons == 0:
            return 0
        
        completed_lessons = LectureProgress.objects.filter(
            user=obj.user,
            lesson__course=obj.course,
            completed=True
        ).count()

        return (completed_lessons / total_lessons) * 100

    def get_lesson_progress(self, obj):
        progress_qs = LectureProgress.objects.filter(
            user=obj.user,
            lesson__course=obj.course
        )
        return LectureProgressSerializer(progress_qs, many=True).data
  
class LectureSerializer(serializers.ModelSerializer):
    """
    Serializer class for each lecture in a course
    """
    
    progress = serializers.SerializerMethodField()
    class Meta:
        model = Lecture
        fields = ['id', 'course','progress', 'title', 'description', 'video_file', 'video_thumbnail', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_progress(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            progress = LectureProgress.objects.filter(lesson = obj).first()
            return LectureProgressSerializer(progress).data if progress else {"completed": False}
        return None

class CourseDetailSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer(many = True, read_only = True)
    instructor = InstructorSerializer(read_only = True)
    class Meta:
        model = Course 
        fields = ['id','instructor', 'title', 'description', 'created_at','price','thumbnail', 'lecture' ]
    


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
 

class PaymentSerializer(serializers.Serializer):
    """Serializer class for each payment"""
    course = CourseSerializer(read_only = True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length = 3)
    source = serializers.CharField(max_length = 255)