from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200) #제목
    content = models.TextField()             #내용
    author = models.ForeignKey(User, on_delete=models.CASCADE) #작성자
    created_at = models.DateTimeField(auto_now=True)           #작성일
    updated_at = models.DateTimeField(auto_now=True)           #수정일
    file = models.FileField(upload_to='files/', blank=True, null=True) #파일

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #어떤 글의 댓글인지
    author = models.ForeignKey(User, on_delete=models.CASCADE) #댓글 작성자
    content = models.TextField()                               #댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)       #작성일

    def __str__(self):
        return self.content
    

