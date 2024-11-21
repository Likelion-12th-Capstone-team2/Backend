from rest_framework import serializers
from .models import *

# 위시리스트 목록에서 객체를 조회하는 시리얼라이저
class WishListGetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Wish
    fields = ['id', 'is_sended', 'item_image', 'heart']

# 위시 아이템을 생성할 때 사용하는 시리얼라이저
class WishPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Wish
    fields = ['id', 'item_name', 'wish_link', 'size', 'color', 'other_option', 'heart']

