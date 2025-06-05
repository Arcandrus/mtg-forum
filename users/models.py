from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds full_name, unique email, and profile picture via Cloudinary.
    """
    full_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='samples/cloudinary-icon'
    )

    @property
    def post_count(self):
        """Returns the count of posts authored by this user."""
        return self.posts.count()

    @property
    def comment_count(self):
        """Returns the count of comments authored by this user."""
        return self.comments.count()

    @property
    def user_status(self):
        """
        Returns a string representing the user's status:
        'Superuser', 'Staff', 'Active', or 'Inactive'.
        """
        if self.is_superuser:
            return "Superuser"
        elif self.is_staff:
            return "Staff"
        elif self.is_active:
            return "Active"
        else:
            return "Inactive"

    def __str__(self):
        return self.username