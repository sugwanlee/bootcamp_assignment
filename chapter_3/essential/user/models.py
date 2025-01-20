from django.db import models
from django.contrib.auth.models import AbstractUser

# User를 커스텀하기 위해 상속
class CustomUser(AbstractUser):
    # 자기소개 필드 추가
    intro = models.TextField()
    # 프로필 이미지 필드 추가
    image = models.ImageField(upload_to="image/", default='default_images/default.png')