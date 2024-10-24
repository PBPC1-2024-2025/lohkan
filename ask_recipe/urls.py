from django.urls import path
from . import views

app_name = 'ask_recipe'

urlpatterns = [
    path('', views.ask_recipe, name='ask_recipe'), 
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    # path('groups/', views.group_list, name='group_list'),
    # path('group/<int:id>/', views.group_detail, name='group_detail'),
    # path('add-chat-message/', views.add_chat_message, name='add_chat_message'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
]
