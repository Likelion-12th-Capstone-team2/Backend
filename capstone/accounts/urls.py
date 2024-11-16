from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
]