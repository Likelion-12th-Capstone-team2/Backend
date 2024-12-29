from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from mypage.models import Category, MyPage
from alarms.models import Alarm
from .serializers import *
from mypage.serializers import CategorySerializer, MyPageSerializer
from alarms.serializers import AlarmPostSerializer
import logging
from django.core.files.base import ContentFile
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from PIL import Image
import io
import urllib.request
from django.http import Http404
# 로거 생성
logger = logging.getLogger('django')
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
    if price == '0':
        wish_items = wish_items.filter(price__lt=30000)

    elif price == '30000':
        wish_items = wish_items.filter(price__gt=29999, price__lt=50000)

    elif price == '50000':
        wish_items = wish_items.filter(price__gt=49999, price__lt=100000)

    elif price == '100000':
        wish_items = wish_items.filter(price__gt=99999)

    elif price is None:
        pass

    else:
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
    logger.debug(f"response: {data}")
    return Response(data=data, status=HTTP_200_OK)

  # 위시 리스트에 아이템 생성
  def post(self, request, user_id):
        # 로그인을 안한 경우 400 오류
        if not request.user.is_authenticated:
            return Response({"error": "로그인 후 위시 아이템을 추가할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)

        # user_id가 현재 접근하고 있는 유저인지 확인
        if user_id != request.user.id:
            return Response({"error": "위시 아이템을 추가할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)

        
        category_id = request.data.get('category')
        logger.debug(f"category id: {category_id}")
        if not Category.objects.filter(id=category_id, user=request.user).exists():
            logger.error("해당 카테고리는 현재 접속한 유저의 카테고리가 아닙니다.")
            return Response({"error": "해당 카테고리는 현재 접속한 유저의 카테고리가 아닙니다."}, status=HTTP_400_BAD_REQUEST)

        logger.debug("Parsed Request data: %s", request.data)

        # item_image 처리
        item_image = request.FILES.get('item_image')
        image_url = request.data.get('item_image')  # URL로 전달된 경우도 확인

        if item_image:  # 파일로 제공된 경우
            data = request.data.copy()
            data['item_image'] = item_image
        elif image_url:  # URL로 제공된 경우
            try:
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                image_data = response.read()

                # 파일이 유효한 이미지인지 확인
                try:
                    Image.open(io.BytesIO(image_data)).verify()
                except (IOError, SyntaxError):
                    logger.error("유효한 이미지 URL이 아닙니다.")
                    return Response({"error": "유효한 이미지 URL이 아닙니다."}, status=HTTP_400_BAD_REQUEST)

                image_name = image_url.split("/")[-1]  # 파일 이름 추출
                image_content = ContentFile(image_data)
                image_content.name = image_name

                data = request.data.copy()
                data['item_image'] = image_content
            except HTTPError as e:
              logger.error(f"HTTPError occurred: {e}")
              return Response({"error": f"HTTPError: {str(e)} - 이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)
            except URLError as e:
              logger.error(f"URLError occurred: {e}")
              return Response({"error": f"URLError: {str(e)} - 이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)
            except Exception as e:
              logger.error(f"Unknown error: {e}")
              return Response({"error": "이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "item_image 또는 유효한 이미지 URL을 제공해야 합니다."}, status=HTTP_400_BAD_REQUEST)

        serializer = WishPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.debug(f"response: {data}")
            return Response(serializer.data, status=HTTP_200_OK)
        logger.error(f"{serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
              

# 특정 위시 아이템 조회, 수정, 삭제 
class WishItemView(views.APIView):
  # 특정 위시 아이템 조회
  def get(self, request, item_id):
    # 현재 접속하고 있는 유저 (wish 주인: owner, 타인: user_id, 로그인하지 않은 경우: guest)
    wishitem = get_object_or_404(Wish, id=item_id)
    wish_items_serializer = WishItemGetSerializer(wishitem)
    user_id = wishitem.user.id
    
    if not request.user.is_authenticated:
      user = 'guest'
    elif user_id == request.user.id:
      user = 'owner'
    else:
      user = request.user.id

    logger.debug(f"user: {user}")

    cateogory = get_object_or_404(Category, id=wish_items_serializer.data['category'])
    cateogory_serializer = CategorySerializer(cateogory)

    # 데이터를 새로 구성
    data = dict(wish_items_serializer.data)
    data['category'] = cateogory_serializer.data['category'] 

    try:
      mypage = get_object_or_404(MyPage, user=wishitem.user)
      mypage_serializer = MyPageSerializer(mypage)
      mypage_serializer_data = mypage_serializer.data
    except Http404:
      mypage_serializer_data = None

    # sender 정보 -> mypage name으로 수정
    if data['sender']:
      logger.debug(f"Attempting to get MyPage for sender: {data['sender']}")
      try:
          sender = get_object_or_404(MyPage, user=int(data['sender']))
          sender_serializer = MyPageSerializer(sender)
          data['sender'] = sender_serializer.data['name']
          logger.debug(f"Sender found: {data['sender']}")
      except Http404:
          logger.warning(f"MyPage not found for sender: {data['sender']}. Using user_id as fallback.")
          data['sender'] = user_id  # MyPage가 없으면 user_id를 사용
    else:
      logger.debug("No sender provided")

    
    response_data = {
      'user': user,
      'item': data,
      'receiver_id': mypage.user.id,
      'setting': mypage_serializer_data
    }

    return Response(data=response_data, status=HTTP_200_OK)

  def patch(self, request, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 위시 아이템을 수정할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    

    wishitem = get_object_or_404(Wish, id=item_id)
    wish_items_serializer = WishItemGetSerializer(wishitem, partial=True)
    user_id = wishitem.user.id



    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 수정할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    



    cateogory = get_object_or_404(Category, id=wish_items_serializer.data['category'])
    cateogory_serializer = CategorySerializer(cateogory)

    # 데이터를 새로 구성
    data = dict(request.data)

      # 이미지 유무에 따른 데이터 변환
    if 'item_image' in data and data['item_image']:
          item_image = request.FILES.get('item_image')
          image_url = request.data.get('item_image')
          if item_image:
            data['item_image'] = item_image
          elif image_url:
            try:
              req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
              response = urllib.request.urlopen(req)
              image_data = response.read()

              try:
                Image.open(io.BytesIO(image_data)).verify()
              except (IOError, SyntaxError):
                return Response({"error": "유효한 이미지 URL이 아닙니다."}, status=HTTP_400_BAD_REQUEST)
              
              image_name = image_url.split("/")[-1]
              image_content = ContentFile(image_data)
              image_content.name = image_name

              data = request.data.copy()
              data['item_image'] = image_content
            
            except HTTPError as e:
              logger.error(f"HTTPError occurred: {e}")
              return Response({"error": f"HTTPError: {str(e)} - 이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)
            except URLError as e:
              logger.error(f"URLError occurred: {e}")
              return Response({"error": f"URLError: {str(e)} - 이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)
            except Exception as e:
              logger.error(f"Unknown error: {e}")
              return Response({"error": "이미지 다운로드 중 오류가 발생했습니다."}, status=HTTP_400_BAD_REQUEST)

          else:
            return Response({"error": "item_image 또는 유효한 이미지 URL을 제공해야 합니다."}, status=HTTP_400_BAD_REQUEST)

    patch_serializer = WishPostSerializer(wishitem, data=data, partial=True)
    if patch_serializer.is_valid():
        patch_serializer.save()
      
        data['category'] = cateogory_serializer.data['category'] 
          
        # sender 정보 -> mypage name으로 수정
        if 'sender' in data and data['sender']:
          logger.debug(f"Attempting to get MyPage for sender: {data['sender']}")
          try:
              sender = get_object_or_404(MyPage, user=int(data['sender']))
              sender_serializer = MyPageSerializer(sender)
              data['sender'] = sender_serializer.data['name']
              logger.debug(f"Sender found: {data['sender']}")
          except Http404:
              logger.warning(f"MyPage not found for sender: {data['sender']}. Using user_id as fallback.")
              data['sender'] = user_id  # MyPage가 없으면 user_id를 사용
        else:
          logger.debug("No sender provided")
          get_serializer = WishItemGetSerializer(wishitem)
          return Response(data=get_serializer.data, status=HTTP_200_OK)
    else:
        return Response({"error": patch_serializer.errors}, status=HTTP_400_BAD_REQUEST)


  def delete(self, request, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 위시 아이템을 삭제할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    wishitem = get_object_or_404(Wish, id=item_id)
    wish_items_serializer = WishItemGetSerializer(wishitem)
    user_id = wishitem.user.id
    # user_id가 현재 접근하고 있는 유저인지 확인
    if user_id != request.user.id:
      return Response({"error": "위시 아이템을 삭제할 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)

    # 해당 아이템이 존재하는지 확인

    # 위시 아이템 삭제
    wishitem.delete()

    return Response({"message": "위시 아이템 삭제 성공!"}, status=HTTP_204_NO_CONTENT)


# 위시 선물 찜하기
class SendView(views.APIView):
  def post(self, request, user_id, item_id):
    logger.debug(f"Authorization Header: {request.headers.get('Authorization')}")

    logger.debug(f"User: {request.user}")
    logger.debug(f"Is authenticated: {request.user.is_authenticated}")
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      logger.debug("로그인 후 선물하기 찜을 선택할 수 있습니다.")
      return Response({"error": "로그인 후 선물하기 찜을 선택할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.id == user_id:
      logger.debug("자기 자신한테 선물할 수 없습니다.")
      return Response({"error": "자기 자신한테 선물할 수 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    try:
      wishitem = get_object_or_404(Wish, id=item_id)

    except Http404:
      logger.debug("위시 아이템이 존재하지 앖습니다.")
      return Response({"error":"위시 아이템이 존재하지 앖습니다."}, status=HTTP_400_BAD_REQUEST)

    if wishitem.is_sended:
      logger.debug("이미 해당 위시 아이템을 선물 받았습니다.")
      return Response({"error":"이미 해당 위시 아이템을 선물 받았습니다."}, status=HTTP_400_BAD_REQUEST)
    
    data = {
      'is_sended': True,
      'sender': request.user.id
    }
    serializer = WishItemGetSerializer(wishitem, data=data, partial=True)

    if serializer.is_valid():
      serializer.save()
    
      # # 알람이 이미 존재하는지 체크
      # user = get_object_or_404(User, id=user_id)
      # existing_alarm = Alarm.objects.filter(
      #   sender=request.user, 
      #   receiver=user, 
      #   item=wishitem
      #   ).exists()  # True/False 반환
      
      # if existing_alarm:
      #   return Response({"message": "이미 동일한 알람이 전송되었으므로 전송되지 않습니다"}, status=HTTP_200_OK)
      
      # 알람 저장하기
      alarm_data = {
                "sender": request.user.id,
                "receiver": user_id,
                "item": wishitem.id,
            }
      alarm_serializer = AlarmPostSerializer(data=alarm_data)
      
      if not alarm_serializer.is_valid():
                logger.debug(f"{alarm_serializer.errors}")
                return Response({"error": alarm_serializer.errors}, status=HTTP_400_BAD_REQUEST)
      alarm_serializer.save()
      return Response(serializer.data, status=HTTP_200_OK)
      

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  
  def delete(self, request, user_id, item_id):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 선물하기 찜을 취소할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    wishitem = get_object_or_404(Wish, id=item_id)

    # 선물 보낸 사람인지 확인
    if wishitem.sender != request.user:
      return Response({"error": "취소 권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)

      # 선물 상태 초기화
    wishitem.is_sended = False
    wishitem.sender = None
    wishitem.save()

    # 관련 알람 삭제
    Alarm.objects.filter(sender=request.user, receiver_id=user_id, item=wishitem).delete()

    return Response({"message": "선물하기 찜 취소 성공!"}, status=HTTP_200_OK)




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


