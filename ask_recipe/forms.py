from django import forms
from .models import RecipeGroup, ChatMessage

# Form untuk membuat dan mengedit grup resep    
class RecipeGroupForm(forms.ModelForm):
    class Meta:
        model = RecipeGroup
        fields = ['name', 'description']

# Form untuk mengirim pesan dalam grup resep
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
