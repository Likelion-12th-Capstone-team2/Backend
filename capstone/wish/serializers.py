from rest_framework import serializers
from .models import *

class WishSerializer(serializers.ModelSerializer):
  class Meta:
    model = Wish
    fields = ['id', 'item_name', 'wish_link', 'size', 'color', 'other_option', 'heart']