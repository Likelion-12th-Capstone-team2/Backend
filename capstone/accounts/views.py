from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import *
from .serializers import *
# Create your views here.

class SignupView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공!', 'data':serializer.data})
        return Response({'messange':'회원가입 실패!', 'error':serializer.errors})
    
class LoginView(views.APIView):
    serializer_class= LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            return Response({'message':'로그인 성공!', 'data':serializer.validated_data})
        return Response({'message':'로그인 실패!', 'error':serializer.errors})