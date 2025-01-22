from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class SignupView(APIView):

    def post(self, request):
        # 입력된 데이터로 객체 생성
        serializer = UserSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            # 데이터베이스의 적용 후 반환값을 user에 저장
            user = serializer.save()
            # 메세지를 json으로 직렬화 후 응답
            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )


class LogoutView(APIView):

    # 인증되지 않은 유저가 접근하면 401에러를 반환
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # body에 입력된 데이터에서 리프레쉬 토큰값을 가져오기
        Refresh_token = request.data.get("refresh")
        
        # 입력된 토큰이 있으면
        if Refresh_token:
            # 토큰의 유효성 검사 후 리프레시 토큰 객체 생성
            token = RefreshToken(Refresh_token)
            # 토큰을 블랙리스트 데이터베이스에 추가
            token.blacklist()
            # 메세지 json형식으로 직렬화 후 응답
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        else:
            # 메세지 json형식으로 직렬화 후 응답
            return Response(
                {"detail": "No token found."}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):

    # 인증되지 않은 유저가 접근하면 401에러를 반환
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 유저 정보로 개웃기네 ORM으로 현재 유저 qurryset 가져오기 
        profile = CustomUser.objects.get(pk=request.user.pk)
        # 시리얼라이저 객체 생성
        serializer = UserSerializer(profile)
        # data를 json으로 직렬화 후 응답
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # 현재 유저 정보로 개웃기네 ORM으로 현재 유저 qurryset 가져오기 
        profile = CustomUser.objects.get(pk=request.user.pk)
        # 시리얼라이저 부분수정 객체 생성
        serializer = UserSerializer(profile, data=request.data, partial=True)
        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            # 데이터베이스에 적용
            serializer.save()
            # data를 json으로 직렬화 후 응답
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
