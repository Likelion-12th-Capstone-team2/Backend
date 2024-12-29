from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alarm
from .serializers import AlarmSerializer
from rest_framework.status import *
# Create your views here.

class AlarmView(APIView):
    def get(self, request):
        user = request.user

        # 유효하지 않은 사용자 처리
        if not user or not user.is_authenticated:
            return Response(
                {"error": "로그인 후 알람을 확인하세요"}, 
                status=HTTP_400_BAD_REQUEST
            )

        # 최신 알림 조회
        alarms = Alarm.objects.filter(receiver=user).order_by('-date')
        serializer = AlarmSerializer(alarms, many=True)

        return Response({
            'message': '알림 조회 성공!',
            'data': serializer.data
        }, status=HTTP_200_OK)