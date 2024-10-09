from django.db import models
from django.contrib.auth.models import User

    
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField() 

    def __str__(self):
        return self.food
    
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField() 
    answer = models.TextField() 
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation with {self.user} on {self.timestamp}'