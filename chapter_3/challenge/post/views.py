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
        # data를 json파일로 직렬화해서 응답
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # 시리얼라이저로 객체 생성
        serializer = PostSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            # author 필드값을 채워준 뒤 데이터베이스에 저장
            serializer.save(author=request.user)
            # data를 json파일로 직렬화해서 응답
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
        # data를 json파일로 직렬화해서 응답
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
                # data를 json파일로 직렬화해서 응답
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
            # data를 json으로 직렬화해서 응답
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
            # 메세지를 json으로 직렬화 후 응답
            return Response(
                {"message": "게시물에 좋아요를 취소하였습니다"},
                status=status.HTTP_200_OK,
            )
        else:
            # 관계형 필드에 유저가 없다면 유저 추가
            post.like.add(request.user)
            # 메세지를 json으로 직렬화 후 응답
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
            # data를 json으로 직렬화 후 응답
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
                # data를 json으로 직렬화 후 응답 
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
            # data를 json으로 직렬화 후 응답
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            # 유저가 다르면 403에러를 반환
            return Response(status=status.HTTP_403_FORBIDDEN)
