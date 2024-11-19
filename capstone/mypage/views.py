from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *

# Create your views here.

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
      return Response(serializer.data, status=HTTP_200_OK)
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
    return Response(serializer.data)

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
      return Response(serializer.data)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  


# Category Post, Get 뷰
class CategoryView(views.APIView):

  # 카테고리 생성
  def post(self, request):
    # 로그인을 안한 경우 400 오류
    if not request.user.is_authenticated:
      return Response({"error": "로그인 후 카테고리를 생성할 수 있습니다."}, status=HTTP_400_BAD_REQUEST)
    
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