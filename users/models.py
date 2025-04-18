from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager

# Create your models here.
def user_profile_picture_path(instance, filename):
    """Generate file path for new user profile picture."""
    return f"profile_pictures/user_{instance.id}/{filename}"

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    is_instructor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
