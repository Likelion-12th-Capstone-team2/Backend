from django.db import models
from accounts.models import User
from wish.models import Wish
from mypage.models import MyPage

# Create your models here.

class Alarm(models.Model):
   sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms_sender') 
   receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms_receiver')
   date = models.DateTimeField(auto_now_add=True)  # 알람이 생성된 시간 자동 저장
   item = models.ForeignKey(Wish,on_delete=models.CASCADE)
   
   def sender_name(self):
        # sender와 연결된 MyPage 객체가 있는 경우 name 반환
        mypage = MyPage.objects.filter(user=self.sender).first()
        return mypage.name if mypage else "No Name"
   
   def __str__(self):
    return f"{self.sender.username} to {self.receiver.username}"