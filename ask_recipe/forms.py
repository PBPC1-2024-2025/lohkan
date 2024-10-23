from django import forms
from .models import RecipeGroup, ChatMessage

class RecipeGroupForm(forms.ModelForm):
    class Meta:
        model = RecipeGroup
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}), 
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
