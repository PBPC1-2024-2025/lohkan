import uuid
from django.db import models
from django.contrib.auth.models import User
    
# Model untuk mengelola grup resep
class RecipeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Model untuk merepresentasikan resep individual
class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID untuk ID unik
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_recipes")
    group = models.OneToOneField(RecipeGroup, on_delete=models.CASCADE, related_name="recipe")  # Setiap resep hanya bisa satu grup
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
# Model untuk merepresentasikan pesan dalam grup resep
class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Tetap pakai UUID jika perlu
    group = models.ForeignKey(RecipeGroup, on_delete=models.CASCADE)  # Many-to-One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'