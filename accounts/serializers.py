from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import json

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
    
    def create(self, validated_data):
        # 이메일 중복 확인
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({
                'status': 401,
                'message': '이미 사용 중인 이메일입니다.'
            })
        
        # 중복되지 않으면 유저 생성
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data): #입력받은 데이터의 유효성을 검증
        email=data.get('email', None)
        password=data.get('password', None)

        if not email or not password:
            raise ValidationError("필수 필드를 모두 입력해주세요.", code=400)

        if not User.objects.filter(email=email).exists():
            raise ValidationError("사용자가 존재하지 않습니다. (등록된 이메일 없음)", code=400)

        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise AuthenticationFailed("잘못된 비밀번호입니다.", code=401)

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        return {
            'id': user.id,
            'username': user.username,
            'access_token': access
        }
        
        
class KakaoLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = User.objects.filter(email=email).first()
        if user:
            # 비밀번호 확인
            if not user.check_password(password):
                raise ValidationError("잘못된 비밀번호입니다.")
        else:
            # 새 사용자 생성
            user = User.objects.create(
                email=email,
                username=f"kakao_{email.split('@')[0]}",
                password=make_password(password),
            )

        return user

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if not email:
            raise serializers.ValidationError('이메일이 필요합니다.')
        if not password:
            raise serializers.ValidationError('비밀번호가 필요합니다.')

        # 사용자가 존재하지 않을 경우 회원가입을 진행하기 때문에 오류를 발생시키지 않음
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise serializers.ValidationError("잘못된 비밀번호입니다.")
        
        return data

