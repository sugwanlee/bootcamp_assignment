from django.db import models
from django.contrib.auth.models import AbstractUser


# 기본유저를 커스텀하여 쓰기 위해 AbstractUser를 상속한 클래스 생성
class CustomUser(AbstractUser):
    # 필드 추가 확장
    intro = models.TextField()
    image = models.ImageField(upload_to="image/", default="default_images/default.png")
