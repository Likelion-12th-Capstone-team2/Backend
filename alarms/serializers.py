from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class AlarmSerializer(serializers.ModelSerializer):
  sender_name = serializers.CharField(source='sender_name', read_only=True)
  date = serializers.SerializerMethodField()
  class Meta:
    model = Alarm
    fields = ['id', 'sender', 'receiver', 'date', 'item', 'sender_name']

    def get_date(self, obj):
        return obj.date.strftime('%Y.%m.%d.')
  