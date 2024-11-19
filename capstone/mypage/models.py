from django.db import models
from accounts.models import User

# Create your models here.
class MyPage(models.Model):
  name = models.CharField(max_length=50)
  background_photo = models.ImageField(upload_to='backgrounds/')
  color = models.CharField(max_length=100)
  typography = models.CharField(max_length=300)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name