from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status 
import logging
# Create your views here.
# 로거 생성
logger = logging.getLogger('django')
# MyPage Post, Get, Patch 뷰
class MypageView(views.APIView):

  #온보딩에서 사용할 mypage 생성
  def post(self, request):

    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 mypage를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # 이미 mypage가 생성된 유저인 경우 400 오류
    if MyPage.objects.filter(user=request.user).exists():
      return Response({"error": "이미 mypage가 생성된 유저입니다."}, status=HTTP_400_BAD_REQUEST)

    serializer = MyPageSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      data = {
        "user": request.user.id,
        "setting": serializer.data
      }
      logger.debug(f'response: {data}')
      return Response(data=data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  def get(self, request):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 mypage를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # mypage가 생성되지 않은 유저인 경우 400 오류
    if not MyPage.objects.filter(user=request.user).exists:
      return Response({"error": "mypage가 생성되지 않은 유저입니다."}, status=HTTP_400_BAD_REQUEST)
    
    # mypage 반환
    mypage = get_object_or_404(MyPage, user=request.user)
    serializer = MyPageSerializer(mypage)

    data = {
      "user": request.user.id,
      "setting": serializer.data
    }

    return Response(data=data, status=HTTP_200_OK)

  def patch(self, request):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 mypage를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # mypage가 생성되지 않은 유저인 경우 400 오류
    if not MyPage.objects.filter(user=request.user).exists:
      return Response({"error": "mypage가 생성되지 않은 유저입니다."}, status=HTTP_400_BAD_REQUEST)
    
    # mypage 반환
    mypage = get_object_or_404(MyPage, user=request.user)
    serializer = MyPageSerializer(mypage, data = request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      data = {
        "user": request.user.id,
        "setting": serializer._data
      }
      logger.debug(f'response: {data}')
      return Response(data=data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  


# Category Post, Get 뷰
class CategoryView(views.APIView):

  # 카테고리 생성
  def post(self, request):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 카테고리를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    if Category.objects.filter(user_id=request.user.id).count() >= 7:
      return Response({"error": "카테고리는 최대 7개까지만 설정 가능합니다."}, status=HTTP_400_BAD_REQUEST)
    
    if Category.objects.filter(user_id=request.user.id, category=request.data['category']).exists():
      return Response({"error": "이미 존재하는 카테고리입니다."}, status=HTTP_400_BAD_REQUEST) 

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  
  def get(self, request):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 카테고리를 불러올 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
    # 로그인한 유저의 카테고리 객체 리스트
    categories = Category.objects.filter(user=request.user)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
  
# 카테고리 수정 (PATCH)
  def patch(self, request, category_id):
        if not request.user.is_authenticated:
            return Response({"error": "로그인 후 카테고리를 수정하세요"}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 카테고리 존재 여부 및 유저 권한 확인
        category = Category.objects.filter(user=request.user, id=category_id).first()
        if not category:
            return Response({"error": "카테고리가 존재하지 않음"}, status=status.HTTP_404_NOT_FOUND)

        # 카테고리 수정
        serializer = CategorySerializer(category, data=request.data, partial=True)  # partial=True로 일부 필드만 수정
        if serializer.is_valid():
            serializer.save()
            return Response(
            {"message": "카테고리 수정 성공!", "data": serializer.data}, 
            status=status.HTTP_200_OK
        )
        return Response(
        {"message": "카테고리 수정 실패", "errors": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

    # 카테고리 삭제 (DELETE)
  def delete(self, request, category_id):
        if not request.user.is_authenticated:
            return Response({"error": "로그인 후 카테고리를 삭제하세요"}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 카테고리 존재 여부 및 유저 권한 확인
        category = Category.objects.filter(user=request.user, id=category_id).first()
        if not category:
            return Response({"error": "카테고리가 존재하지 않음"}, status=status.HTTP_404_NOT_FOUND)

        # 카테고리 삭제
        category.delete()
        return Response({"message": "카테고리 삭제 성공!"}, status=status.HTTP_204_NO_CONTENT)