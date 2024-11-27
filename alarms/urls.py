from django.urls import path, include
from .views import *

app_name = 'alarms'

urlpatterns = [
    path('', AlarmView.as_view(), name='alarm_list'),
]