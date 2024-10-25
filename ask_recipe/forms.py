from django import forms
from .models import Recipe, ChatMessage

class RecipeGroupForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4, 'cols': 40}), 
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
