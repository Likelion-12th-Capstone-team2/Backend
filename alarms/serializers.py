from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class AlarmSerializer(serializers.ModelSerializer):
  sender = serializers.SerializerMethodField()  # sender 필드를 커스텀 처리
  class Meta:
    date = serializers.SerializerMethodField()

    model = Alarm
    fields = ['id', 'sender', 'receiver', 'date', 'item']

    def get_date(self, obj):
        return obj.date.strftime('%Y.%m.%d.')
    
    def get_sender(self, obj):
        return obj.sender.username  # sender의 이름(username)을 반환

