# 필수과제
## 과제 개요
- 필수과제에서는 FBV를 선택
- 기능 구현에 중심을 두고 과제를 수행
- 필수과제는 아니지만 댓글 기능, 좋아요 기능도 추가로 구현

## 1.User 앱
1. 사용자 모델 구현
    
    기본 Django User 모델을 확장하여 커스텀 필드 추가 (예: 프로필 이미지, 소개글)
    
    - `CustomUser`
    
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
        - template: `user/signup.html`<br>
![Image](https://github.com/user-attachments/assets/5c6316a5-74f4-487e-bb57-1ac9da0bad5d)
        
        
    
    <br>

    2. 로그인
    
    - view: `login` or `LoginView`
    
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
        
    - template: `user/login.html`<br>
![Image](https://github.com/user-attachments/assets/87ca29e0-bd88-4711-b53f-9bf463656066)
        


    <br>

    3. 로그아웃
    - view: `logout` or `LogoutView`
        ```py
        @require_POST
        def logout(request):
            # 로그인 세션 삭제
            auth_logout(request)
            # 로그인 로직 실행
            return redirect("user:login")
        ```

<br>
<br>

3. 사용자 프로필 페이지 구현
    - view: `user_profile` or `UserProfileView`
        ```py
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
        ```

    - template: `user/profile.html`<br>
        ![Image](https://github.com/user-attachments/assets/7d949399-09e4-4dbf-b6d6-8046c34207ab)

<br>

## 2.Post 앱 (CRUD)

1. Post 모델 구현
    
    필드: 제목, 내용, 작성자, 작성일, 수정일
    - `Post`
        ```py
        from django.db import models

        # Post 테이블 생성
        class Post(models.Model):
            # CustomUser의 1대다 필드 생성
            author = models.ForeignKey("user.CustomUser",on_delete=models.CASCADE, related_name="authors")
            # 제목
            title = models.CharField(max_length=50)
            # 내용
            content = models.TextField()
            # 글 생성 시간
            created_at = models.TimeField(auto_now_add=True)
            # 글 수정 시간
            updated_at = models.TimeField(auto_now=True)
            
            # 좋아요 필드 생성
            like = models.ManyToManyField("user.CustomUser", related_name="likes", blank=True)
        ```


2. 게시판 기능
    1. 게시글 목록 보기 (Read - List)
        - view: `post_list` or `PostListView`
            ```py
            def post_list(request):
                # 모든 게시글 정보(QuerySet) 가져오기
                posts = Post.objects.all()
                context = {
                    "posts" : posts
                }
                # 필요한 데이터를 담아서 응답
                return render(request, "post/post_list.html", context)
            ```

        - template: `post/post_list.html`<br>
        ![Image](https://github.com/user-attachments/assets/2b639bb8-5be5-45a4-9ba3-99e0099f2c56)

        <br>

    2. 게시글 상세 보기 (Read - Detail)
        - view: `post_detail` or `PostDetailView`

            ```py
            def post_detail(request, pk):
                # 단일 게시글 정보(QuerySet) 가져오기
                post = Post.objects.get(pk=pk)
                comment_form = CommentForm()
                liked = post.like.filter(pk=request.user.pk).exists()
                context = {
                    "post" : post,
                    "comment_form" : comment_form,
                    "liked" : liked,
                }
                # 필요한 데이터를 담아서 응답
                return render(request, "post/post_detail.html", context)
            ```

        - template: `post/post_detail.html`<br>
        ![Image](https://github.com/user-attachments/assets/f832b66b-3e3a-45ae-a028-0aff63ddb3eb)

        <br>

    3. 게시글 작성 기능 (Create)
        - view: `post_create` or `PostCreateView`
            ```py
            # 로그인 상태일 때만 허용
            @login_required
            # "GET", "POST" 요청일 때만 허용
            @require_http_methods(["GET","POST"])
            def post_create(request):
                if request.method == "POST":
                    # 입력된 게시글 정보로 form 객체 생성
                    form = PostForm(request.POST)
                    # 유효성 검사
                    if form.is_valid():
                        # 저장하기에 필요한 데이터(author)가 부족하기 때문에 폼 데이터를 데이터베이스에 저장하기 전에 post 객체 생성
                        post = form.save(commit=False)
                        # 저장에 필요한 author 테이블에 로그인중인 유저정보 입력
                        post.author = request.user
                        # 데이터베이스에 저장
                        post.save()
                        # 게시글 목록 로직 호출
                        return redirect("post:post_list")
                else:
                    # 게시글 작성을 위해 빈 폼 생성
                    form = PostForm()
                context = {
                    "form" : form
                }
                # 필요한 데이터를 담아서 응답
                return render(request, "post/post_form.html", context)
            ```

        - template: `post/post_form.html`<br>
        ![Image](https://github.com/user-attachments/assets/84cd2f7c-cba1-43bb-8c6c-3060aabb0ed7)


        <br>

    4. 게시글 수정 기능 (Update)
        - view: `post_update` or `PostUpdateView`
            ```py
            # 로그인 중일 때만 허용
            @login_required
            # "GET", "POST" 요청일 때만 허용
            @require_http_methods(["GET","POST"])
            def post_update(request, pk):
                # 수정할 게시글 정보(QuerySet) 가져오기
                post = Post.objects.get(pk=pk)
                # 게시글 작성자와 현재 수정을 요청하는 유저가 같은지 검사
                if request.user == post.author:
                    if request.method == "POST":
                        # 입력된 데이터로 수정된 데이터 폼 생성
                        form = PostForm(request.POST, instance=post)
                        # 유효성 검사
                        if form.is_valid():
                            # 저장하기에 필요한 데이터(author)가 부족하기 때문에 폼 데이터를 데이터베이스에 저장하기 전에 post 객체 생성
                            post = form.save(commit=False)
                            # 저장에 필요한 author 테이블에 로그인중인 유저정보 입력
                            post.author = request.user
                            # 데이터베이스에 저장
                            post.save()
                            # 수정된 페이지를 보여주기 위해 상세페이지지 로직 호출
                            return redirect("post:post_detail", pk)
                    else:
                        # 현재 수정 할 게시글의 데이터를 포함한 객체 생성
                        posts = PostForm(instance=post)
                    context = {
                        "posts" : posts,
                        "post" : post
                    }
                    # 필요한 데이터를 담아서 응답
                    return render(request, "post/post_form.html", context)
            ```

        - template: `post/post_form.html` (작성 기능과 공유)<br>
        ![Image](https://github.com/user-attachments/assets/18dd1ffd-c89f-4e25-9ead-570fcf3844f6)


    5. 게시글 삭제 기능 (Delete)
        - view: `post_delete` or `PostDeleteView`

            ```py
            # 로그인 중일 때만 허용
            @login_required
            # "GET", "POST" 요청일 때만 허용
            @require_http_methods(["GET","POST"])
            def post_delete(request, pk):
                # 삭제할 게시글 가져오기
                post = Post.objects.get(pk=pk)
                if request.method == "POST":
                    # 게시글 데이터베이스에서 삭제
                    post.delete()
                    # 게시글 목록 로직 호출
                    return redirect("post:post_list")
                context = {
                    "post" : post
                }
                # 삭제 하기 전 마지막 확인 페이지 응답
                return render(request, "post/post_confirm_delete.html", context)
            ```
        
        - template: `post/post_confirm_delete.html`<br>
        ![Image](https://github.com/user-attachments/assets/23ff0a66-dfb3-469c-a4b1-19fc289838c9)