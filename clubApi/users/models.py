from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Remove username field completely
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Add custom fields
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    
    # Set email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Use custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email