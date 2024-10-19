from django.db import models
import uuid
from django.contrib.auth.models import User

# Model Article dan Comment
class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title = models.CharField(max_length=255, null=False) 
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)  

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)