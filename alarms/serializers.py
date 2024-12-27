from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class AlarmSerializer(serializers.ModelSerializer):
  sender = serializers.SerializerMethodField()  # sender를 커스터마이징
  class Meta:
    date = serializers.SerializerMethodField()

    model = Alarm
    fields = ['id', 'sender', 'receiver', 'date', 'item']

    def get_date(self, obj):
        return obj.date.strftime('%Y.%m.%d.')
    
    def get_sender(self, obj):
        return obj.sender.username  # User 모델의 username 반환