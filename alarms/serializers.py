from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class AlarmSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()  # 수정: sender_name 메서드 호출
    date = serializers.SerializerMethodField()

    def get_sender(self, obj):
        mypage = MyPage.objects.filter(user=obj.sender).first()
        return mypage.name if mypage else "No Name"

    def get_date(self, obj):
        return obj.date.strftime('%Y.%m.%d.')

    class Meta:
        model = Alarm
        fields = ['id', 'sender', 'receiver', 'date', 'item']  
    
class AlarmPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Alarm
    fields = ['id', 'sender', 'receiver', 'date', 'item']
  