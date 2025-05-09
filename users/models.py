from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Full name of the user
    full_name = models.CharField(max_length=255, blank=True, null=True)

    # Email address (already included in AbstractUser, but we redefine it here)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username