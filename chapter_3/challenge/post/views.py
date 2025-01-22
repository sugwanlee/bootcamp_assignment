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
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)    


    def get(self, request, pk):
        post = self.get_object(pk)
        Serializer = PostSerializer(post)
        return Response(Serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        post = self.get_object(pk)
        if post.author == request.user:
            Serializer = PostSerializer(post, data=request.data, partial=True)
            if Serializer.is_valid(raise_exception=True):
                Serializer.save()
                return Response(Serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.author == request.user:
            post.delete()
            data = {"result" : f'{post.title} is deleted'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class PostLikeView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.like.filter(pk=request.user.pk).exists():
            post.like.remove(request.user)
            return Response({"message": "게시물에 좋아요를 취소하였습니다"}, status=status.HTTP_200_OK)
        else:
            post.like.add(request.user)
            return Response({"message": "게시물에 좋아요를 했습니다!"}, status=status.HTTP_200_OK)
        
        
class CommentView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    # POST요청일 때는 Post테이블의 pk값을 가져온다
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # PUT요청일 때는 Comment테이블의pk 값을 가져온다
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:    
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    # DELETE요청일 때는 Comment테이블의pk 값을 가져온다
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            comment.delete()
            data = {"result" : f'{comment.post.title}의 댓글이 삭제되었습니다.'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)