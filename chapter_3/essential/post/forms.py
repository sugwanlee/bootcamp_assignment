from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ("author",)

    widgets = {
        'content': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
    }