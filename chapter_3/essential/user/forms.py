
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

# 회원가입 할 때 확장한 필드를 추가하기 위해 커스텀
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # 가입에 필요한 필수 필드 및 이미지 필드 가져오기(이미지 필드는 필수값 아님)
        fields = ("username", "password1", "password2", "intro", "image")
