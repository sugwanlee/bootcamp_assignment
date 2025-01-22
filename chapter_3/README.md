# 필수과제
## 1.User 앱
1. 사용자 모델 구현
    
    기본 Django User 모델을 확장하여 커스텀 필드 추가 (예: 프로필 이미지, 소개글)
    
    - `CustomUser`
    
    models.py
    ```py
    from django.db import models
    from django.contrib.auth.models import AbstractUser

    # User를 커스텀하기 위해 상속
    class CustomUser(AbstractUser):
        # 자기소개 필드 추가
        intro = models.TextField()
        # 프로필 이미지 필드 추가
        image = models.ImageField(upload_to="image/", default='default_images/default.png')
    ```

2. 회원가입, 로그인, 로그아웃 기능 구현
    1. 회원가입
        - view: `signup` or `SignUpView`
        - template: `user/signup.html`

    ```py
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
    ```
    
    <br>

    2. 로그인
    - view: `login` or `LoginView`
    - template: `user/login.html`

    ```py
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
    ```