from django.db import models
from accounts.models import User

# Create your models here.

# 마이페이지 모델
class MyPage(models.Model):
<<<<<<< HEAD
  name = models.CharField(max_length=50)
#   background_photo = models.ImageField(upload_to='backgrounds/')
  background_photo = models.ImageField(upload_to='images/')
=======
  name = models.CharField(max_length=6)
  background_photo = models.ImageField(upload_to='backgrounds/')
>>>>>>> edaf257edc8143be61cdd2fb4fd50006b8cc42af
  color = models.CharField(max_length=100)
  typography = models.CharField(max_length=300)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  

# 카테고리 모델
class Category(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.CharField(max_length=11)