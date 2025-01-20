from django import forms
from .models import Post, Comment

# ModelForm으로 모델에 맞는 폼 생성
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = "__all__"
        # ForeignKey 값 제외
        exclude = ("author","like")

# 입력한 "content"에서 줄바꿈 가능하게 바꿈
    widgets = {
        'content': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
    }
    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("post", "author")