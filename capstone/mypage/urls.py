from django.urls import path
from django.conf import settings
from mypage.views import *

app_name = 'mypage'

urlpatterns=[
  path('', MypageView.as_view()),
    
]