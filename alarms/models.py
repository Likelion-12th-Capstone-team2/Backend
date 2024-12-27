from django.db import models
from accounts.models import User
from wish.models import Wish

# Create your models here.

class Alarm(models.Model):
   sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms_sender') 
   receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms_receiver')
   date = models.DateTimeField(auto_now_add=True)  # 알람이 생성된 시간 자동 저장
   item = models.ForeignKey(Wish,on_delete=models.CASCADE)
   
   def sender_name(self):
        return self.sender.username  # sender가 User 객체로 연결되어 있어야 함
   
   def __str__(self):
    return f"{self.sender.username} to {self.receiver.username}"