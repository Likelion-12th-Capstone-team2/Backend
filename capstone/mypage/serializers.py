from rest_framework import serializers
from .models import *

# MyPage 시리얼라이저
class MyPageSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyPage
    fields = ['id', 'name', 'background_photo', 'color', 'typography']


# Category 시리얼라이저
class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'category']