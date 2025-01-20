from django.urls import path
from . import views

# 네임스페이스 지정
app_name = "user"
urlpatterns = [
    # 회원기능 urls
    path("signup/",views.signup, name="signup"),
    path("login/",views.login, name="login"),
    path("logout/",views.logout, name="logout"),
    # 프로필 urls
    path("user_profile/", views.user_profile, name="user_profile"),
]
