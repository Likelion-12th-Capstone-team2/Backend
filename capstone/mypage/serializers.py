from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
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