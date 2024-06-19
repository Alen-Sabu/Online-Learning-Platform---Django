from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _ 

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and username
    is the unique identifier
    """

    def create_user(self, email, username, password, **extra_fields):
        """
        Function to create a normal user
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        
        email = self.normalize_email(email)

        if self.filter(email = email).exists():
            raise ValueError("This email address already exists")
        if self.filter(username = username).exists():
            raise ValueError("This username already exists")
        
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        """
        Function to create an admin
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be is_staff = True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be is_superuser = True"))
        return self.create_user(email, username, password, **extra_fields)