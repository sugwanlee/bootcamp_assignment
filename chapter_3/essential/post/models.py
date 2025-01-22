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


class Comment(models.Model):
    
    # Post와 일대다 관계 설정
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    # CustomUser와 일대다 관계 설정
    author = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)    