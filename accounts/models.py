from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.username:  # username이 없는 경우 기본값 설정
            self.username = f"user_{self.email.split('@')[0]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
