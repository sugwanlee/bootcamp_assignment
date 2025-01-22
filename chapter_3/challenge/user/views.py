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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated]
        
    def post(self, request):
        
        Refresh_token = request.data.get('refresh')
        if Refresh_token:
            token = RefreshToken(Refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No token found."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = CustomUser.objects.get(pk=request.user.pk)
        serializer = UserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile = CustomUser.objects.get(pk=request.user.pk)
        serializer = UserSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)