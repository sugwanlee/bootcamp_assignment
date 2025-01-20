from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view()),
    path("<int:pk>/", views.PostDetailView.as_view()),
    path("<int:pk>/like/", views.PostLikeView.as_view()),
    path("<int:pk>/comment/", views.CommentView.as_view()),
]