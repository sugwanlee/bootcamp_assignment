from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    return render(request, "post/post_list.html", context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post" : post
    }
    return render(request, "post/post_detail.html", context)


@login_required
@require_http_methods(["GET","POST"])
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post:post_list")
    else:
        form = PostForm()
    context = {
        "form" : form
    }
    return render(request, "post/post_form.html", context)


@login_required
@require_http_methods(["GET","POST"])
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("post:post_detail", pk)
        else:
            posts = PostForm(instance=post)
        context = {
            "posts" : posts,
            "post" : post
        }
        return render(request, "post/post_form.html", context)


@login_required
@require_http_methods(["GET","POST"])
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post:post_list")
    context = {
        "post" : post
    }
    return render(request, "post/post_confirm_delete.html", context)
