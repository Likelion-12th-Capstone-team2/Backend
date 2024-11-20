from django.db import models
from accounts.models import User
from mypage.models import Category

# Create your models here.

# 위시아이템 모델
class Wish(models.Model):
  # wish로 설정한 유저 정보
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  is_sended = models.BooleanField(default=False)
  # 준 유저 정보
  sender = models.ForeignKey(User, on_delete=models.CASCADE)

  wish_link = models.CharField(max_length=10000)
  item_image = models.ImageField(upload_to='items/')
  item_name = models.CharField(max_length=1000)
  size = models.CharField(max_length=100, null=True)
  color = models.CharField(max_length=100, null=True)
  other_option = models.CharField(max_length=100, null=True)
  heart = models.IntegerField()

  #카테고리 정보
  category = models.ManyToManyField(Category)

  def __str__(self):
    return self.name
