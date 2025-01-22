from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required

# "GET", "POST" 요청만 허용
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        # 입력한 데이터를 form 객체로 생성, request.FILES == 이미지 파일
        form = CustomUserCreationForm(request.POST, request.FILES)
        # 유효성 검사
        if form.is_valid():
            # 데이터 베이스에 적용
            form.save()
            # 로그인 페이지로 이동
            return redirect("user:login")
    else:
        # 회원가입을 위한 빈 페이지를 form 객체로 생성
        form = CustomUserCreationForm()
    context = {
        "form" : form
    }
    # 필요한 데이터를 담아서 응답
    return render(request, "user/signup.html", context)


# "GET", "POST" 요청만 허용
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        # 사용자 입력 데이터 검증 폼 생성
        form = AuthenticationForm(data=request.POST)
        # 유효성 검사
        if form.is_valid():
            # 사용자 세션 생성 및 세션_id 브라우저에 저장
            auth_login(request, form.get_user())
            # 게시글 목록 페이지지 로직 실행
            return redirect("post:post_list")
    else:
        # 사용자 입력 폼 생성
        form = AuthenticationForm()
    context = {
        "form" : form
    }
    # 필요한 데이터를 담아서 응답
    return render(request, "user/login.html", context)


# "POST" 요청일 때만 혀용
@require_POST
def logout(request):
    # 로그인 세션 삭제
    auth_logout(request)
    # 로그인 로직 실행
    return redirect("user:login")



# "GET" 요청 일때만 허용
@require_GET
def user_profile(request):
    # url로 접근하는걸 막기위해 url로 pk값을 가져오지 않고, request.user.pk 값을 이용함
    profile = CustomUser.objects.get(pk=request.user.pk)
    context = {
        "profile" : profile
    }
    # 필요한 데이터를 담아서 응답
    return render(request, "user/profile.html", context)