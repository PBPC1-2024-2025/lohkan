from django.contrib.auth.models import User
from django.db import models
import uuid

class RecipeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Tambahkan UUID
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Tambahkan UUID
    group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Tambahkan UUID
    group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'