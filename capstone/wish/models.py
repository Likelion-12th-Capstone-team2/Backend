from django.db import models
from accounts.models import User
from mypage.models import Category

# Create your models here.

# 위시아이템 모델
class Wish(models.Model):
  # wish로 설정한 유저 정보
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

  is_sended = models.BooleanField(default=False)
  # 준 유저 정보
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', null=True)

  wish_link = models.URLField(null=True, blank=True)
  item_image = models.ImageField(upload_to='items/')
  item_name = models.CharField(max_length=1000)
  price = models.IntegerField()
  size = models.CharField(max_length=100, null=True)
  color = models.CharField(max_length=100, null=True)
  other_option = models.CharField(max_length=100, null=True)
  heart = models.IntegerField()

  #카테고리 정보
  category = models.ForeignKey(Category, on_delete=models.PROTECT)

  def __str__(self):
    return self.item_name 
  #반환값이 name으로 되어 있어서 item_name으로 수정하였음
