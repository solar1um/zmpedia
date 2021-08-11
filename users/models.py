from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profiles', default='user.jpeg')
    descriptions = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 1920 or img.width > 1080:
            output_size = (1920, 1080)
            img.thumbnail(output_size)
            img.save(self.image.path)
