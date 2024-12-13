from django.urls import path
from . import views

app_name = 'ask_recipe'

# kumpulan URL untuk nampilin page atau views yang sesuai
urlpatterns = [
    path('', views.ask_recipe, name='ask_recipe'), 
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('send_message/', views.send_message, name='send_message'),
    path('messages/<uuid:group_id>/', views.get_messages, name='get_messages'),
    path('delete_group/<uuid:group_id>/', views.delete_group, name='delete_group'),
    path('delete_message/<uuid:message_id>/', views.delete_message, name='delete_message'),
    path('search/', views.search_recipe, name='search_recipe'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('create_recipe_flutter/', views.create_recipe_flutter, name='create_recipe_flutter'),
    path('update_recipe_flutter/<uuid:recipe_id>/', views.update_recipe_flutter, name='update_recipe_flutter'),    
    path('delete_recipe/<uuid:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
