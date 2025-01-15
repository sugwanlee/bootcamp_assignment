from django.db import models

class Post(models.Model):
    author = models.ForeignKey("user.CustomUser",on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
# Create your models here.
