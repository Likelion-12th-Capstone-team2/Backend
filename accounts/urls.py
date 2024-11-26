from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    #path('kakao/', kakao_login, name='kakao_login'),  # 카카오 로그인 URL 추가
    
    #path('kakao/callback/', kakao_callback, name='kakao_callback'),
    #path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('kakao/', KakaoLoginView.as_view()),
    path('kakao/login/callback/',KakaoCallbackView.as_view()),
    path('kakao/signup/', KakaoSignupView.as_view()),
]