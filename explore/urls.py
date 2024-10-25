from django.urls import path
from explore.views import show_explore, add_food, edit_food, delete_food, show_xml, add_food_ajax, show_json

app_name = 'explore'

urlpatterns = [
    path('explore', show_explore, name='show_explore'),
    path('add-food/', add_food, name='add_food'),
    path('edit-food/<uuid:id>', edit_food, name='edit_food'),
    path('delete-food/<uuid:id>', delete_food, name='delete_food'),
    path('xml/', show_xml, name='show_xml'),
    path('add-food-ajax/', add_food_ajax, name='add_food_ajax'),
    path('json/', show_json, name='show_json'),
]