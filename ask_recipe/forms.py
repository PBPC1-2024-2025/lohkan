from django import forms
from .models import Recipe

# Form untuk membuat dan mengedit grup resep    
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'cooking_time', 'servings']
