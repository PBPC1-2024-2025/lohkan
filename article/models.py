from django.db import models
import uuid
from django.contrib.auth.models import User

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title = models.CharField(max_length=255, null=False) 
    description = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  

    def __str__(self):
        return self.name
    
    
