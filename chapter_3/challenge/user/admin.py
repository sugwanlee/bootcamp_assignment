from django.contrib import admin
from .models import CustomUser

# 관리자 페이지에서 관리할 테이블 설정
admin.site.register(CustomUser)
