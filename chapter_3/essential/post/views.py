from django.shortcuts import render
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required


def post_list(request):
    # 모든 게시글 정보(QuerySet) 가져오기
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    # 필요한 데이터를 담아서 응답
    return render(request, "post/post_list.html", context)


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

# "POST" 요청만 허용
@require_POST
def post_like(request, pk):
    # 사용자가 로그인 중일 때
    if request.user.is_authenticated:
        # 게시글 가져오기
        post = Post.objects.get(pk=pk)
        # 유저가 좋아요를 이미 눌렀는지 확인
        if post.like.filter(pk=request.user.pk).exists():
            # 좋아요 삭제
            post.like.remove(request.user)
        else:
            # 좋아요 추가
            post.like.add(request.user)
        # 게시글 페이지 로직 실행
        return redirect("post:post_detail", pk)
    else:
        # 로그인 페이지 로직 실행
        return redirect("user:login")
    
# "POST" 요청만 허용
@require_POST
def comment_create(request, pk):
    # 사용자가 로그인 중일 때
    if request.user.is_authenticated:
        # 게시글 가져오기
        post = Post.objects.get(pk=pk)
        # 코멘트 폼에 댓글정보 넣기
        form = CommentForm(request.POST)
        # 유효성 검사
        if form.is_valid():
            # 데이터베이스에 적용 전 정보로 객체 생성
            comment = form.save(commit=False)
            # 관계 필드정보 넣어주기
            comment.post = post
            comment.author = request.user
            # 데이터베이스에 적용
            comment.save()
            # 게시물 페이지 로직 실행
            return redirect("post:post_detail", pk)
    else:
        # 로그인 페이지 로직 실행
        return redirect("user:login")


def comment_update(request ,post_pk ,comment_pk):
    # 수정할 코멘트의 게시물 가져오기
    post = Post.objects.get(pk=post_pk)
    # 코멘트 가져오기
    comment = Comment.objects.get(pk=comment_pk)
    # 코멘트 작성자가 현재 유저랑 일치 할 때
    if comment.author == request.user:
        if request.method == "POST":
            # 수정할 정보 객체를 생성
            form = CommentForm(request.POST, instance=comment)
            # 유효성 검사
            if form.is_valid():
                # 데이터베이스에 적용 전 정보로 객체 생성
                updated_comment = form.save(commit=False)
                # 관계 필드정보 넣어주기
                updated_comment.author = request.user
                updated_comment.post = post
                # 데이터베이스에 적용
                updated_comment.save()
                # 게시물 페이지 로직 실행
                return redirect("post:post_detail", post_pk)
        else:
            # 수정할 원래 댓글내용을 객체로 생성
            comment_update_form = CommentForm(instance=comment)
            # 상세 페이지에 필요한 정보를 컨텍스트에 담음
            context = {
                "post" : post,
                "comment_update_form" : comment_update_form,
                "comment_pk" : comment_pk
            }
            # 필요한 데이터를 담아서 응답
            return render(request, "post/post_detail.html", context)
        

def comment_delete(request, comment_pk):
    # 삭제할 코멘트 가져오기
    comment = Comment.objects.get(pk=comment_pk)
    # 작성자와 현재 유저가 같으면
    if comment.author == request.user:
        # 삭제
        comment.delete()
        # 게시물 페이지 로직 실행
        return redirect("post:post_detail", comment.post_id)