from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # 시리얼라이저가 참조할 모델 설정
        model = CustomUser
        # 참조할 필드 설정
        fields = ["email", "username", "password", "intro", "image"]
        # 특정필드를 어떻게 접근할지 설정
        extra_kwargs = {"password": {"write_only": True}}

    # 오버라이딩
    def create(self, validated_data):
        # 입력된 "username"을 이용해 새 CustomUser 객체 생성
        user = CustomUser(
            username=validated_data["username"],
        )
        # 입력받은 "password"를 해싱해 객체에 입력
        user.set_password(validated_data["password"])
        # 데이터베이스에 저장
        user.save()
        # 객체 반환
        return user
