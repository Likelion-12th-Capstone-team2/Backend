from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from mypage.models import Category
from .serializers import *
from mypage.serializers import CategorySerializer

class WishView(views.APIView):
  # 위시 리스트 조회
  def get(self, request, user_id):

    # 내 페이지인지 확인
    is_owner = False
    if request.user.id == user_id:
      is_owner = True
    
    # 카테고리 목록 조회
    category_list = Category.objects.filter(user=user_id)

    # 위시 아이템 목록 조회
    wish_items = Wish.objects.filter(user=user_id).order_by('heart')

    # 쿼리 파라미터 조회
    price = request.GET.get('price')
    category = int(request.GET.get('category'))

    # 가격대별 필터링
    match price:
      case '0':
        wish_items = wish_items.filter(price__lt=30000)

      case '30,000':
        wish_items = wish_items.filter(price__gt=29999, price__lt=50000)

      case '50,000':
        wish_items = wish_items.filter(price__gt=49999, price__lt=100000)

      case '100,000':
        wish_items = wish_items.filter(price__gt=99999)

      case None:
        pass

      case _:
        return Response({"error": "가격 범위 설정이 잘못되었습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # 카테고리
    if category:
      if category_list.filter(id=category).exists():
        
        wish_items = wish_items.filter(category=category)
      else:
        return Response({"error": "존재하지 않는 category입니다."}, status=HTTP_400_BAD_REQUEST)
    
    category_serializer = CategorySerializer(category_list, many=True)
    wish_items_serializer = WishListGetSerializer(wish_items, many=True)

    data = {
      'is_owner': is_owner,
      'catagory': category_serializer.data,
      'wish_items': wish_items_serializer.data
    }
    
    return Response(data=data, status=HTTP_200_OK)

  # 위시 리스트에 아이템 생성
  def post(self, request, user_id):
    
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 mypage를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 추가할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    serializer = WishPostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.error, status=HTTP_400_BAD_REQUEST)

  


# # 특정 위시 아이템 조회, 수정, 삭제 
# class WishItemView(views.APIView):
    
#   # 특정 위시 아이템 조회
#   def get(self, pk, pk):

#   def patch(self, request, pk):

#   def delete(self,pk):