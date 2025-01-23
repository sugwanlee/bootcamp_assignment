### 1. DRF(Django Rest Framework)로 변환

- User와 Post 앱을 API로 변환
- Serializer 구현
    - `UserSerializer`
        ```py
        from rest_framework import serializers
        from .models import CustomUser


        class UserSerializer(serializers.ModelSerializer):

            class Meta:
                # 시리얼라이저가 참조할 모델 설정
                model = CustomUser
                # 참조할 필드 설정
                fields = ["email", "username", "password", "intro", "image"]
                # 특정필드를 어떻게 접근할지 설정
                extra_kwargs = {"password": {"write_only": True}}

            # 오버라이딩
            def create(self, validated_data):
                # 입력된 "username"을 이용해 새 CustomUser 객체 생성
                user = CustomUser(
                    username=validated_data["username"],
                )
                # 입력받은 "password"를 해싱해 객체에 입력
                user.set_password(validated_data["password"])
                # 데이터베이스에 저장
                user.save()
                # 객체 반환
                return user

        ```


    - `PostSerializer`
        ```py
        from rest_framework import serializers
        from .models import Post, Comment


        class PostSerializer(serializers.ModelSerializer):
            # get_like_count() 호출하고 객체 생성
            like_count = serializers.SerializerMethodField()
            # get_comments() 호출하고 객체 생성
            comments = serializers.SerializerMethodField()

            # class Meta 오버라이딩
            class Meta:
                # 직렬화할 데이터의 기반이 되는 모델 설정
                model = Post
                # 직렬화 대상 필드 지정
                fields = "__all__"
                # 읽기 전용 필드 지정
                read_only_fields = [
                    "author",
                ]

            # obj == Post
            def get_like_count(self, obj):
                # 정참조를 이용해서 Post의 like 테이블과 관련있는 유저의 수를 카운팅
                return obj.like.count()

            def get_comments(self, obj):
                # 역참조를 이용해 post와 관련 있는 Comment테이블의 정보를 다 가져오기기
                comments = obj.comments.all()
                # 쿼리셋셋에서 파이썬 자료구조로 직렬화
                return CommentSerializer(comments, many=True).data



        class CommentSerializer(serializers.ModelSerializer):

            # class Meta 오버라이딩
            class Meta:
                # 직렬화할 데이터의 기반이 되는 모델 설정
                model = Comment
                # 직렬화 대상 필드 지정
                fields = "__all__"
                # 읽기 전용 필드 지정
                read_only_fields = [
                    "post",
                    "author",
                ]
        ```

- APIView 사용하여 CRUD 기능 구현
    ```py
    from django.shortcuts import get_object_or_404, render
    from .models import Post, Comment
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from rest_framework import status
    from .serializers import PostSerializer, CommentSerializer


    class PostListView(APIView):

        # 인증되지 않은 유저가 접근하면 401에러를 반환
        permission_classes = [IsAuthenticated]

        def get(self, request):
            # ORM으로 Posts 객체 생성
            posts = Post.objects.all()
            # 시리얼라이저 객체 생성
            serializer = PostSerializer(posts, many=True)
            data = serializer.data
            # 'like_count'와 'comments' 필드를 제거
            for post in data:
                post.pop('like_count', None)
                post.pop('comments', None)
            # data를 json파일로 형식변환 후 응답
            return Response(data, status=status.HTTP_200_OK)

        def post(self, request):
            # 시리얼라이저로 객체 생성
            serializer = PostSerializer(data=request.data)
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                # author 필드값을 채워준 뒤 데이터베이스에 저장
                serializer.save(author=request.user)
                # data를 json파일로 형식변환 후 응답
                return Response(serializer.data, status=status.HTTP_201_CREATED)


    class PostDetailView(APIView):
        
        # 인증되지 않은 유저가 접근하면 401에러를 반환
        permission_classes = [IsAuthenticated]

        # 공통되는 코드 함수로 정의
        def get_object(self, pk):
            return get_object_or_404(Post, pk=pk)

        def get(self, request, pk):
            # 게시글 qurryset 가져오기
            post = self.get_object(pk)
            # 시리얼라이저 객체 생성
            Serializer = PostSerializer(post)
            # data를 json파일로 형식변환 후 응답
            return Response(Serializer.data, status=status.HTTP_200_OK)

        def put(self, request, pk):
            # 게시글 qurryset 가져오기
            post = self.get_object(pk)
            # 현재 유저와 게시글 작성자가 일치하는지 확인
            if post.author == request.user:
                # 부분수정 객체 생성
                Serializer = PostSerializer(post, data=request.data, partial=True)
                # 유효성 검사
                if Serializer.is_valid(raise_exception=True):
                    # 데이터베이스 적용
                    Serializer.save()
                    # data를 json파일로 형식변환 후 응답
                    return Response(Serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                # 일치하지 않으면 403에러 반환
                return Response(status=status.HTTP_403_FORBIDDEN)

        def delete(self, request, pk):
            # 삭제할 게시물 qurryset 가져오기
            post = self.get_object(pk)
            # 현재 유저와 게시글 작성자가 일치하는지 확인 
            if post.author == request.user:
                # 삭제
                post.delete()
                # 메세지를 전달하기 위해 딕셔너리 생성
                data = {"result": f"{post.title} is deleted"}
                # data를 json으로 형식변환 후 응답
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                # 일치하지 않으면 403에러 반환
                return Response(status=status.HTTP_403_FORBIDDEN)


    class PostLikeView(APIView):
        
        # 인증되지 않은 유저가 접근하면 401에러를 반환    
        permission_classes = [IsAuthenticated]

        def post(self, request, pk):
            # 게시물 qurryset 가져오기
            post = get_object_or_404(Post, pk=pk)
            # 게시물의 like 관계형 필드에 현재 유저가 있는지 확인
            if post.like.filter(pk=request.user.pk).exists():
                # 관계형 필드에서 유저 삭제
                post.like.remove(request.user)
                # 메세지를 json으로 형식변환환 후 응답
                return Response(
                    {"message": "게시물에 좋아요를 취소하였습니다"},
                    status=status.HTTP_200_OK,
                )
            else:
                # 관계형 필드에 유저가 없다면 유저 추가
                post.like.add(request.user)
                # 메세지를 json으로 형식변환 후 응답
                return Response(
                    {"message": "게시물에 좋아요를 했습니다!"}, status=status.HTTP_200_OK
                )


    class CommentView(APIView):
        
        # 인증되지 않은 유저가 접근하면 401에러를 반환
        permission_classes = [IsAuthenticated]

        # POST요청일 때는 Post테이블의 pk값을 가져온다
        def post(self, request, pk):
            # 게시물 qurryset 가져오기
            post = get_object_or_404(Post, pk=pk)
            # 입력된 데이터로 시리얼라이저 객체 생성
            serializer = CommentSerializer(data=request.data)
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                # 리드온리인 관계형 필드에 필요한 값을 pk값과 request.user를 이용해 적절한 데이터를 넣어주기
                serializer.save(author=request.user, post=post)
                # data를 json으로 형식변환 후 응답
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # PUT요청일 때는 Comment테이블의pk 값을 가져온다
        def put(self, request, pk):
            # 코멘트의 qurryset 가져오기
            comment = get_object_or_404(Comment, pk=pk)
            # 현재 유저와 코멘트 작성자가 같은지 확인
            if comment.author == request.user:
                # 부분 수정 객체 시리얼라이저 생성
                serializer = CommentSerializer(comment, data=request.data, partial=True)
                # 유효성 검사
                if serializer.is_valid(raise_exception=True):
                    # 데이터베이스에 적용
                    serializer.save()
                    # data를 json으로 형식변환 후 응답 
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                # 유저가 다르면 403에러를 반환
                return Response(status=status.HTTP_403_FORBIDDEN)

        # DELETE요청일 때는 Comment테이블의pk 값을 가져온다
        def delete(self, request, pk):
            # 코멘트의 qurryset 가져오기
            comment = get_object_or_404(Comment, pk=pk)
            # 현재 유저와 코멘트 작성자가 같은지 확인
            if comment.author == request.user:
                # 삭제
                comment.delete()
                # 메세지를 딕셔너리 형태로 생성
                data = {"result": f"{comment.post.title}의 댓글이 삭제되었습니다."}
                # data를 json으로 형식변환 후 응답
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                # 유저가 다르면 403에러를 반환
                return Response(status=status.HTTP_403_FORBIDDEN)

    ```
    - READ
    ![Image](https://github.com/user-attachments/assets/f85269ab-9845-459a-884e-a15264fc3952)
    ![Image](https://github.com/user-attachments/assets/efaa0267-0223-47b9-a64b-54e58abf25b5)

    - CREATE
    ![Image](https://github.com/user-attachments/assets/465b0102-ac54-45d8-805b-4c937fc378bf)

    - UPDATE
    ![Image](https://github.com/user-attachments/assets/ba43d39f-1450-41f6-aaa9-c2b20040697e)

    - DELETE
    ![Image](https://github.com/user-attachments/assets/7dcbbc2b-bb7e-466f-8aae-bcc49b36f872)


- URL 설정 및 라우팅
    `user/urls.py`
    ```py
    urlpatterns = [
        path("signup/", views.SignupView.as_view()),
        # simplejwt 내장 뷰 사용
        path("signin/", TokenObtainPairView.as_view()),
        # simplejwt 내장 뷰 사용
        path("token/refresh/", TokenRefreshView.as_view()),
        path("logout/", views.LogoutView.as_view()),
        path("user_profile/", views.ProfileView.as_view()),
    ]
    ```
    `post/urls.py`
    ```py
    urlpatterns = [
        path("", views.PostListView.as_view()),
        path("<int:pk>/", views.PostDetailView.as_view()),
        path("<int:pk>/like/", views.PostLikeView.as_view()),
        path("<int:pk>/comment/", views.CommentView.as_view()),
    ]

    ```

### 2. 좋아요 기능

- Post 모델에 좋아요 필드 추가
    ```py
    class Post(models.Model):

        # CustomUser와 일대다 관계 설정
        author = models.ForeignKey(
            "user.CustomUser", on_delete=models.CASCADE, related_name="posts"
        )
        title = models.CharField(max_length=50)
        content = models.TextField()
        created_at = models.TimeField(auto_now_add=True)
        updated_at = models.TimeField(auto_now=True)
        # CustomUser와 다대다 관계 설정
        like = models.ManyToManyField("user.CustomUser", related_name="likes", blank=True)
    ```
    like 필드가 좋아요 필드
    <br>

- 좋아요 개수 표시
    ```py
    class PostSerializer(serializers.ModelSerializer):
        # get_like_count() 호출하고 객체 생성
        like_count = serializers.SerializerMethodField()
        # get_comments() 호출하고 객체 생성
        comments = serializers.SerializerMethodField()

        # class Meta 오버라이딩
        class Meta:
            # 직렬화할 데이터의 기반이 되는 모델 설정
            model = Post
            # 직렬화 대상 필드 지정
            fields = "__all__"
            # 읽기 전용 필드 지정
            read_only_fields = [
                "author",
            ]

        # obj == Post
        def get_like_count(self, obj):
            # 정참조를 이용해서 Post의 like 테이블과 관련있는 유저의 수를 카운팅
            return obj.like.count()

        def get_comments(self, obj):
            # 역참조를 이용해 post와 관련 있는 Comment테이블의 정보를 다 가져오기기
            comments = obj.comments.all()
            # 쿼리셋셋에서 파이썬 자료구조로 직렬화
            return CommentSerializer(comments, many=True).data
    ```
    `like_count = serializers.SerializerMethodField()` 여기서 get_like_count()를 호출해서 좋아요 갯수를 가져옴

### 3. 댓글 기능

- Comment 모델 구현
    - `Comment`
        ```py
        class Comment(models.Model):

            # Post와 일대다 관계 설정
            post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
            # CustomUser와 일대다 관계 설정
            author = models.ForeignKey(
                "user.CustomUser", on_delete=models.CASCADE, related_name="comments"
            )
            content = models.TextField()
            created_at = models.TimeField(auto_now_add=True)
            updated_at = models.TimeField(auto_now=True)

        ```

- 댓글 기능
    - 댓글 작성(2번 게시글에 댓글작성)
    ![Image](https://github.com/user-attachments/assets/04be9702-db17-49da-8df8-5f2e89ac075a)

    - 댓글 수정(3번 댓글 수정정)
    ![Image](https://github.com/user-attachments/assets/b264c0b4-9239-4740-b486-c2082d2b7d95)

    - 댓글 삭제(4번 댓글을 삭제하고, 어디 게시글에서 삭제되었는지 게시글 title과 메세지 출력)
    ![Image](https://github.com/user-attachments/assets/fd3de936-e282-45c2-b000-44a200cbb9d1)

- 게시글 상세 페이지에 댓글 목록 표시
    ```py
    class PostSerializer(serializers.ModelSerializer):
        # get_like_count() 호출하고 객체 생성
        like_count = serializers.SerializerMethodField()
        # get_comments() 호출하고 객체 생성
        comments = serializers.SerializerMethodField()

        # class Meta 오버라이딩
        class Meta:
            # 직렬화할 데이터의 기반이 되는 모델 설정
            model = Post
            # 직렬화 대상 필드 지정
            fields = "__all__"
            # 읽기 전용 필드 지정
            read_only_fields = [
                "author",
            ]

        # obj == Post
        def get_like_count(self, obj):
            # 정참조를 이용해서 Post의 like 테이블과 관련있는 유저의 수를 카운팅
            return obj.like.count()

        def get_comments(self, obj):
            # 역참조를 이용해 post와 관련 있는 Comment테이블의 정보를 다 가져오기기
            comments = obj.comments.all()
            # 쿼리셋셋에서 파이썬 자료구조로 직렬화
            return CommentSerializer(comments, many=True).data
    ```
    `comments = serializers.SerializerMethodField()` 여기서 get_comments()를 호출해서    댓글 정보 가져옴
    ![Image](https://github.com/user-attachments/assets/efaa0267-0223-47b9-a64b-54e58abf25b5)

### 4. 데이터베이스

- SQLite3에서 PostgreSQL or MySQL로 마이그레이션
    ```py
    # postgreSQL로 DB변경
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "challenge_db",     # db 이름
            "USER": "dltnrhks1",        # 관리자 id
            "PASSWORD": "sugwan1599",   # 관리자 비번
            "HOST": "localhost",
            "PORT": "",
        }
    }
    ```
    - pgAdmin 에서 확인 가능능
![Image](https://github.com/user-attachments/assets/62917616-61c0-42f7-b1a7-a0d0d03dafdf)