from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alarm
from .serializers import AlarmSerializer
from rest_framework.status import *
# Create your views here.

class AlarmView(APIView):
    def get(self, request):
        user = request.user  # 현재 로그인된 사용자

        # 로그인을 안한 경우 400 오류
        if not user.is_authenticated:
            return Response({"error": "로그인 후 알람을 확인하세요"}, status=HTTP_400_BAD_REQUEST)

        # 최신 알림이 먼저 오게 함
        alarms = Alarm.objects.filter(receiver=user).order_by('-date')  # 수신자가 현재 사용자
        serializer = AlarmSerializer(alarms, many=True)  # 여러 객체 직렬화
        
        return Response({
            'message': '알림 조회 성공!',
            'data': serializer.data
        })