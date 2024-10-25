import uuid
from django.db import models
from django.contrib.auth.models import User

class RecipeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID untuk ID unik
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Grup dibuat oleh user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID untuk ID unik
    group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Resep ditambahkan oleh user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Tetap pakai UUID jika perlu
    group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)  # Many-to-One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'