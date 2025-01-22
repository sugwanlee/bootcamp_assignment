from django.db import models


class Post(models.Model):
    
    # CustomUser와 일대다 관계 설정
    author = models.ForeignKey("user.CustomUser",on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    # CustomUser와 다대다 관계 설정
    like = models.ManyToManyField("user.CustomUser", related_name="likes", blank=True)


class Comment(models.Model):
    
    # Post와 일대다 관계 설정
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    # CustomUser와 일대다 관계 설정
    author = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)