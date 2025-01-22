from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 회원기능 url
urlpatterns = [
    path("signup/", views.SignupView.as_view()),
    # simplejwt 내장 뷰 사용
    path("signin/", TokenObtainPairView.as_view()),
    # simplejwt 내장 뷰 사용
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("user_profile/", views.ProfileView.as_view()),
]
