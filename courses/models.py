from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

User = get_user_model()

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_("Bio"), blank=True)
    profile_picture = models.ImageField(upload_to='instructors/', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user.email
    
class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(_("course title"), max_length=255)
    description = models.TextField(_("course description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
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

    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self) -> str:
        return f"{self.user.email} enrolled in {self.course.title}"
    

class Payment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Payment for {self.course.title} - {self.amount}"