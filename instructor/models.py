from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

# Create your models here.

User = get_user_model()

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_("Bio"), blank=True)
    profile_picture = models.ImageField(upload_to='instructors/', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user.email
