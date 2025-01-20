from django.urls import path
from . import views

# 네임스페이스 생성
app_name = "post"
urlpatterns = [
    # 게시글 CRUD url
    path("", views.post_list, name="post_list"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("update/<int:pk>/", views.post_update, name="post_update"),
    path("delete/<int:pk>/", views.post_delete, name="post_delete"),
    # 좋아요 url
    path("like/<int:pk>/", views.post_like, name= "post_like"),
    # 댓글 CUD url
    path("<int:pk>/comment/create", views.comment_create, name="comment_create"),
    path("<int:post_pk>/comment/<int:comment_pk>/update", views.comment_update, name="comment_update"),
    path("comment/<int:comment_pk>/delete", views.comment_delete, name="comment_delete"),
    
]
