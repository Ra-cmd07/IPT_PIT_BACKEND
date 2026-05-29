from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os

# Simple file storage fallback
class FallbackMediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', os.path.join(os.path.dirname(__file__), 'media'))
        super().__init__(*args, **kwargs)

MediaCloudinaryStorage = FallbackMediaStorage


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='userprofile/', null=True, blank=True, storage=MediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
