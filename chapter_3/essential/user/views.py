from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = CustomUserCreationForm()
    context = {
        "form" : form
    }
    return render(request, "user/signup.html", context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("post:post_list")
    else:
        form = AuthenticationForm()
    context = {
        "form" : form
    }
    return render(request, "user/login.html", context)


@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect("user:login")


require_GET
def user_profile(request, pk):
    profile = CustomUser.objects.get(pk=pk)
    context = {
        "profile" : profile
    }
    return render(request, "user/profile.html", context)