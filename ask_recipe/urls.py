from django.urls import path
from . import views

app_name = 'ask_recipe'

urlpatterns = [
    path('', views.ask_recipe, name='ask_recipe'), 
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('send_message/', views.send_message, name='send_message'),
    path('messages/<uuid:group_id>/', views.get_messages, name='get_messages'),
    path('delete_group/<uuid:group_id>/', views.delete_group, name='delete_group'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
]
