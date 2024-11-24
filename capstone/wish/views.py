from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from mypage.models import Category, MyPage
from .serializers import *
from mypage.serializers import CategorySerializer, MyPageSerializer

class WishView(views.APIView):
  # 위시 리스트 조회
  def get(self, request, user_id):

    # 현재 접속하고 있는 유저 (wish 주인: owner, 타인: user_id, 로그인하지 않은 경우: guest)
    if not request.user.is_authenticated:
      user = 'guest'
    elif user_id == request.user.id:
      user = 'owner'
    else:
      user = request.user.id
    
    # 카테고리 목록 조회
    category_list = Category.objects.filter(user=user_id)

    # 위시 아이템 목록 조회
    wish_items = Wish.objects.filter(user=user_id).order_by('heart')

    # 쿼리 파라미터 조회
    price = request.GET.get('price')
    category = request.GET.get('category')

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
      if category_list.filter(id=int(category)).exists():
        
        wish_items = wish_items.filter(category=int(category))
      else:
        return Response({"error": "존재하지 않는 category입니다."}, status=HTTP_400_BAD_REQUEST)
    
    category_serializer = CategorySerializer(category_list, many=True)
    wish_items_serializer = WishListGetSerializer(wish_items, many=True)

    page = get_object_or_404(MyPage, user=user_id)
    mypage_serializer = MyPageSerializer(page)

    data = {
      'user': user,
      'catagory': category_serializer.data,
      'wish_items': wish_items_serializer.data,
      'setting': mypage_serializer.data
    }
    
    return Response(data=data, status=HTTP_200_OK)

  # 위시 리스트에 아이템 생성
  def post(self, request, user_id):
    
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 위시 아이템을 추가할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 추가할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    serializer = WishPostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  


# 특정 위시 아이템 조회, 수정, 삭제 
class WishItemView(views.APIView):
  # 특정 위시 아이템 조회
  def get(self, request, user_id, item_id):
    # 현재 접속하고 있는 유저 (wish 주인: owner, 타인: user_id, 로그인하지 않은 경우: guest)
    if not request.user.is_authenticated:
      user = 'guest'
    elif user_id == request.user.id:
      user = 'owner'
    else:
      user = request.user.id

    wishitem = get_object_or_404(Wish, id=item_id)
    wish_items_serializer = WishItemGetSerializer(wishitem)

    cateogory = get_object_or_404(Category, id=wish_items_serializer.data['category'])
    cateogory_serializer = CategorySerializer(cateogory)

    # 데이터를 새로 구성
    data = dict(wish_items_serializer.data)
    data['category'] = cateogory_serializer.data['category'] 

    page = get_object_or_404(MyPage, user=user_id)
    mypage_serializer = MyPageSerializer(page)

      
    response_data = {
      'user': user,
      'item': data,
      'setting': mypage_serializer.data
    }

    return Response(data=response_data, status=HTTP_200_OK)

  def patch(self, request, user_id, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 위시 아이템을 수정할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 수정할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    wishitem = get_object_or_404(Wish, id=item_id)
    wish_items_serializer = WishItemGetSerializer(wishitem, data=request.data, partial=True)

    if wish_items_serializer.is_valid():
      wish_items_serializer.save()

      cateogory = get_object_or_404(Category, id=wish_items_serializer.data['category'])
      cateogory_serializer = CategorySerializer(cateogory)

      # 데이터를 새로 구성
      data = dict(wish_items_serializer.data)
      data['category'] = cateogory_serializer.data['category'] 
        
      

      return Response(data=data, status=HTTP_200_OK)
    
    else:
      return Response({"error": wish_items_serializer.errors}, status=HTTP_400_BAD_REQUEST)

  def delete(self, request, user_id, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 위시 아이템을 삭제할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 삭제할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)

    # 해당 아이템이 존재하는지 확인
    wishitem = get_object_or_404(Wish, id=item_id)

    # 위시 아이템 삭제
    wishitem.delete()

    return Response({"message": "위시 아이템 삭제 성공!"}, status=HTTP_204_NO_CONTENT)

# 위시 선물 찜하기
class SendView(views.APIView):
  def post(self, request, user_id, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 mypage를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.id == user_id:
      return Response({"error": "자기 자신한테 선물할 수 없습니다."}, status=HTTP_400_BAD_REQUEST)

    wishitem = get_object_or_404(Wish, id=item_id)
    
    data = {
      'is_sended': True,
      'sender': request.user.id
    }
    serializer = WishItemGetSerializer(wishitem, data=data, partial=True)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#다른 사람 위시리스트의 위시 -> 내 위시리스트로 가져오기
class ToMyWishView(views.APIView):
  def get(self, request, item_id):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
      return Response(
                {"message": "로그인이 필요합니다. 로그인 페이지로 이동하세요."}, 
                status=HTTP_401_UNAUTHORIZED
            )
        
    try:
      target_wish = Wish.objects.get(id=item_id)
    except Wish.DoesNotExist:
      return Response({"error": "불러올 아이템이 존재하지 않습니다"}, status = HTTP_404_NOT_FOUND)
    
    if target_wish.user == request.user:
      return Response({"error":"이미 본인의 위시 아이템으로 등록되어 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    #불러온 wish 정보를 반환
    serializer = ToMyWishSerializer(target_wish)
    return Response(serializer.data, status=HTTP_200_OK)
