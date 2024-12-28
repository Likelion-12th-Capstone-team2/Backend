from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alarm
from .serializers import AlarmSerializer
from rest_framework.status import *
# Create your views here.

class HealthView(APIView):
    def get(self, request):
        return Response(status=HTTP_200_OK)