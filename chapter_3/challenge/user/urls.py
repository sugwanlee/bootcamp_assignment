from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "user"
urlpatterns = [
    path("signup/",views.SignupView.as_view()),
    path("signin/", TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path("logout/",views.LogoutView.as_view()),
    path("user_profile/", views.ProfileView.as_view()),
]
