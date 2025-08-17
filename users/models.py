from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    You can add additional fields here if needed.
    """

    # Example of an additional field
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    is_agency = models.BooleanField(default=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
