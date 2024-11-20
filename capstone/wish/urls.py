from django.urls import path
from django.conf import settings
from .views import *

app_name = 'wish'

urlpatterns=[
  path('<int:user_id>/', .as_view()),   
]