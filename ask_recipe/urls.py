from django.urls import path
from . import views

app_name = 'ask_recipe'

urlpatterns = [
    path('', views.ask_recipe, name='ask_recipe'), 
    path('create_recipe/', views.create_recipe_group, name='create_recipe_group'),
    path('groups/', views.group_list, name='group_list'),
    path('group/<int:id>/', views.group_detail, name='group_detail'),
    path('add-chat-message/', views.add_chat_message, name='add_chat_message'),
]
