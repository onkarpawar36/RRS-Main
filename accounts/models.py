from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_picture and hasattr(self.profile_picture, 'path'):
            # Skip resizing for default image
            if 'default.jpg' not in self.profile_picture.name:
                try:
                    # Resize image if it's too large
                    img = Image.open(self.profile_picture.path)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(self.profile_picture.path)
                except (FileNotFoundError, OSError):
                    # Handle cases where the file might not exist or be corrupted
                    pass

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default_profile.svg'
