from django.shortcuts import render, redirect
import requests
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import *
from .serializers import *
import os 
from dotenv import load_dotenv
import requests
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import AuthenticationFailed, ValidationError

# Create your views here.

class SignupView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        # validation error 처리 시 status와 message 포함
        formatted_errors = []
        for field, error_list in serializer.errors.items():
            for error in error_list:
                formatted_errors.append({
                    'status': 400,  # 원하는 상태 코드 설정
                    'field': field,
                    'message': error
                })

        return Response({'message': '회원가입 실패!', 'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                return Response({'message': '로그인 성공!', 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': '로그인 실패!', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({'message': '로그인 실패!', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# 환경 변수 로드 (옵션: .env 파일을 사용)
load_dotenv()

KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
KAKAO_PASSWORD = os.environ.get('KAKAO_PASSWORD')
KAKAO_CLIENT_SECRET_KEY = os.environ.get('KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')
KAKAO_LOGIN_URI = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URI = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URI = "https://kapi.kakao.com/v2/user/me"

class KakaoLoginView(views.APIView):
    def get(self, request):
        kakao_url =f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
        return redirect(kakao_url)

class KakaoCallbackView(views.APIView):
    def get(self, request):

        code = request.GET.get('code') #access_token 발급 위함
        if not code:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        # 로드된 client_id 확인
        print(f"KAKAO_CLIENT_ID: {KAKAO_CLIENT_ID}")

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': KAKAO_REDIRECT_URI,
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post("https://kauth.kakao.com/oauth/token", data=request_data, headers=token_headers)

        if token_res.status_code != 200:
            return Response({'message': 'Access token 발급 실패', 'error': token_res.json()}, status=HTTP_400_BAD_REQUEST)
        
        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=HTTP_400_BAD_REQUEST)

        auth_headers = { # 사용자 정보 불러오기
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.post(KAKAO_PROFILE_URI, headers=auth_headers)
        if user_info_res.status_code != 200:
            return Response({'message': '정보 불러오기 실패'}, status=HTTP_400_BAD_REQUEST)

        user_info_json = user_info_res.json()
        social_id = str(user_info_json.get('id'))
        email = user_info_json.get('kakao_account', {}).get('email')

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(email=email) 
            # kakao계정 아이디가 이미 가입한거라면
            # 서비스에 rest-auth 로그인
            data={'email':email,'password':KAKAO_PASSWORD}
            serializer = KakaoLoginSerializer(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['exist'] = True
                # 로그인 후 발급된 access token과 함께 응답
                validated_data['access_token'] = access_token
                
                return Response({'message': "카카오 로그인 성공", 'data': validated_data}, status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # 카카오 회원가입으로 리다이렉트
            return redirect(f'/accounts/kakao/signup/?email={email}')

class KakaoSignupView(views.APIView):
    def get(self, request):  
        # 쿼리 매개변수에서 email 가져오기
        email = request.GET.get('email', None)
        if not email:
            return Response({'message': '이메일 정보가 없습니다.'}, status=HTTP_400_BAD_REQUEST)

        # 회원가입 데이터를 구성
        request_data = {
            'email': f"{email}",  # KakaoUser prefix 추가
            'password': KAKAO_PASSWORD,  # 미리 정의된 카카오 비밀번호 사용
        }

        # KakaoLoginSerializer를 사용하여 회원가입 처리
        serializer = KakaoLoginSerializer(data=request_data)
        if serializer.is_valid():
            user = serializer.save()

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_data = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'access_token': access_token,  # 로그인 후 사용할 access token
                } 
            return Response({'message': '카카오계정 통한 회원가입 및 로그인 완료', 'data': user_data}, status=HTTP_201_CREATED)
        return Response({'message': '카카오계정 통한 회원가입 오류', 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    