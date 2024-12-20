from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'cooking_time', 'servings', 'image']

    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time is not None and cooking_time <= 0:
            raise forms.ValidationError("Cooking time must be greater than 0.")
        return cooking_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if servings is not None and servings <= 0:
            raise forms.ValidationError("Number of servings must be greater than 0.")
        return servings