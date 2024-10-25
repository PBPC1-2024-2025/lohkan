from django.urls import path
from . import views

app_name = 'ask_recipe'

urlpatterns = [
    path('', views.ask_recipe, name='ask_recipe'), 
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
]
