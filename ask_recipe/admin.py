from django.contrib import admin
from .models import RecipeGroup, Recipe, ChatMessage

# Register your models here.
admin.site.register(RecipeGroup)
admin.site.register(Recipe)
admin.site.register(ChatMessage)