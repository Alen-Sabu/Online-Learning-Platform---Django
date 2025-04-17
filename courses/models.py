from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 
from instructor.models import Instructor
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def default_course_image():
    return 'default/default_course.png'

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    title = models.CharField(_("course title"), max_length=255)
    description = models.TextField(_("course description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True, default=default_course_image)

    def __str__(self) -> str:
        return self.title

class UserCourseInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.TextField()
    learning_goals = models.TextField()

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lecture')
    title = models.CharField(_("lecture title"), max_length=255)
    description = models.TextField(_("lecture description"))
    video_file = models.FileField(upload_to='lecutres/',blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='lecture-thumbnails/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self) -> str:
        return f"{self.user.email} enrolled in {self.course.title}"
    
    def update_progress(self):
        total_lectures = self.course.lecture.count()
        completed_lectures = LectureProgress.objects.filter(user = self.user, lecture__course = self.course, completed = True).count()
        if total_lectures > 0:
            self.progress = (completed_lectures / total_lectures) * 100
        else:
            self.progress = 0.0
        self.save()

    
class LectureProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress', null= True, blank=True)
    lesson = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default = 0)
    

    class Meta:
        unique_together = ('user', 'lesson')
class Payment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Payment for {self.course.title} - {self.amount}"