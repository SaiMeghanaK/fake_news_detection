from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
class User(AbstractUser):
    ROLE_CHOICES = (
        ("writer", "Writer"),
        ("reader", "Reader"),
    )
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return f"{self.email} ({self.role})"