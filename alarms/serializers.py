from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class AlarmSerializer(serializers.ModelSerializer):
  sender = serializers.CharField(source='sender_name')
  class Meta:
    date = serializers.SerializerMethodField()

    model = Alarm
    fields = ['id', 'sender', 'receiver', 'date', 'item']

    def get_date(self, obj):
        return obj.date.strftime('%Y.%m.%d.')
  