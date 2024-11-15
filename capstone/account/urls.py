from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
]